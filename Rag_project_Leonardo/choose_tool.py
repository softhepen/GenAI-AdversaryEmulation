import os
import json
import re
import time
import requests
from collections import defaultdict

from utils.config import TEMPLATE_FOLDER, RAG_MODEL
from utils.template_handler import load_template
from utils.logger import get_logger
#from utils.tokenizer import tokenizer
from utils.utils import (
    extract_valid_tool_names,
    enrich_result_with_technique_names,
    normalize_tactic_formatting,
    filter_result_by_strict_tool_list
)

# Initialize logger for this module
logger = get_logger()

RAG_API_URL = os.environ.get("RAG_API_URL", "http://localhost:8000/v1/completions")
RAG_API_TIMEOUT = float(os.environ.get("RAG_API_TIMEOUT", "60"))
RAG_API_MAX_RETRIES = int(os.environ.get("RAG_API_MAX_RETRIES", "3"))
RAG_API_BACKOFF_SECONDS = float(os.environ.get("RAG_API_BACKOFF_SECONDS", "2"))

def _post_llm_request(prompt: str, model: str) -> str:
    """
    Sends the compiled prompt to vLLM (OpenAI-compatible REST API) and returns the text output.
    """
    payload = {
        "model": model,          
        "prompt": prompt,
        "max_tokens": 1024,
        "temperature": 0.0
    }

    last_error = None
    for attempt in range(1, RAG_API_MAX_RETRIES + 1):
        try:
            response = requests.post(
                RAG_API_URL,
                json=payload,
                timeout=RAG_API_TIMEOUT,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code != 200:
                last_error = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"LLM REST API failed (attempt {attempt}/{RAG_API_MAX_RETRIES}): {last_error}")
            else:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["text"].strip()

                logger.error(f"Unexpected API response format: {data}")
                last_error = "Unexpected API response format"
        except requests.Timeout:
            last_error = f"Timeout after {RAG_API_TIMEOUT}s"
            logger.error(f"LLM REST API timeout (attempt {attempt}/{RAG_API_MAX_RETRIES}): {last_error}")
        except requests.RequestException as e:
            last_error = str(e)
            logger.error(f"LLM REST API request error (attempt {attempt}/{RAG_API_MAX_RETRIES}): {last_error}")

        if attempt < RAG_API_MAX_RETRIES:
            time.sleep(RAG_API_BACKOFF_SECONDS)

    return f"LLM Error: {last_error or 'Unknown error'}"

def normalize_tool_name(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())

def is_valid_ttp_entry(entry):
    meta = entry.get("metadata", {})
    tactic_ids = meta.get("tactic", [])
    tactic_names = meta.get("tactic_name", [])
    tech_id = entry.get("technique")
    tech_name = meta.get("technique_name")
    desc = meta.get("description")

    return all([
        tactic_ids, tactic_names, tech_id,
        tech_name and str(tech_name).strip(),
        desc and str(desc).strip()
    ])

def group_ttps_detailed_by_tactic(ttp_entries):
    grouped = defaultdict(lambda: {
        "tactic_name": None,
        "techniques": defaultdict(lambda: {
            "technique_name": None,
            "descriptions": []
        })
    })

    for entry in ttp_entries:
        if not is_valid_ttp_entry(entry):
            continue

        meta = entry["metadata"]
        tactic_ids = meta["tactic"]
        tactic_names = meta["tactic_name"]
        tech_id = entry["technique"]
        tech_name = str(meta["technique_name"]).strip()
        desc = str(meta["description"]).strip()

        for tid, tname in zip(tactic_ids, tactic_names):
            tactic = grouped[tid]
            tactic["tactic_name"] = tname
            technique = tactic["techniques"][tech_id]
            technique["technique_name"] = tech_name
            technique["descriptions"].append(desc)

    return grouped

def evaluate_tool_precision(raw_output, valid_tools, logger=None):
    normalized_valid_tools = {
        normalize_tool_name(tool): tool for tool in valid_tools
    }

    tool_lines = re.findall(r"Tool:\s*(.+)", raw_output)
    predicted_tools = [
        normalize_tool_name(t.strip()) for t in tool_lines if t.strip().lower() != "no tool"
    ]

    tp = [normalized_valid_tools[t] for t in predicted_tools if t in normalized_valid_tools]
    fp = [t for t in predicted_tools if t not in normalized_valid_tools]

    precision = len(tp) / (len(tp) + len(fp)) if (tp or fp) else 1.0

    if logger:
        logger.info(f"Tool field precision: {precision:.2f}")

    return {
        "precision": precision,
        "true_positives": tp,
        "false_positives": fp,
        "total_tools": len(predicted_tools),
        "total_entries": len(tool_lines)
    }

def format_detailed_ttps_for_prompt(grouped_ttps):
    lines = []
    for tid, tactic_data in grouped_ttps.items():
        if not tactic_data["tactic_name"]:
            continue
        lines.append(f"- Tactic: {tid} – {tactic_data['tactic_name']}")
        for tech_id, tech_data in tactic_data["techniques"].items():
            if not tech_data["technique_name"]:
                continue
            lines.append(f"  Technique: {tech_id} – {tech_data['technique_name']}")
            if tech_data["descriptions"]:
                lines.append(f"  Description: {' '.join(tech_data['descriptions'])}")
    return "\n".join(lines)

def build_technique_name_map(ttp_entries):
    mapping = {}
    for entry in ttp_entries:
        meta = entry.get("metadata", {})
        tech_id = entry.get("technique")
        tech_name = meta.get("technique_name")
        if tech_id and tech_name:
            mapping[tech_id] = tech_name.strip()
    return mapping

def run_tool_matching_prompt(ttp_text, tool_text, template_name="template_match.txt", model=RAG_MODEL):
    try:
        prompt_path = os.path.join(os.path.dirname(__file__), TEMPLATE_FOLDER, template_name)
        template_text = load_template(prompt_path)
        compiled_prompt = template_text.replace("{{ ttp_list }}", ttp_text).replace("{{ tool_list }}", tool_text)

        output = _post_llm_request(compiled_prompt, model)
        return output.strip()
    except Exception as e:
        logger.error(f"Tool matching prompt failed: {e}")
        return ""

def match_from_text_files(ttps_path, tools_path, output_path, template_name="template_match.txt"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    logger.info("TTP extraction from CTI report")
    try:
        with open(ttps_path, "r", encoding="utf-8") as f:
            ttp_data = json.load(f)
        grouped_ttps = group_ttps_detailed_by_tactic(ttp_data)
        ttp_text = format_detailed_ttps_for_prompt(grouped_ttps)
        technique_map = build_technique_name_map(ttp_data)

        ttp_list_path = os.path.join(os.path.dirname(output_path), "ttp_list.txt")
        with open(ttp_list_path, "w", encoding="utf-8") as f:
            f.write(ttp_text)
    except Exception as e:
        logger.error(f"Error loading or processing TTPs from {ttps_path}: {e}")
        return None

    try:
        with open(tools_path, "r", encoding="utf-8") as f:
            tool_text = f.read().strip()

        tool_name_path = os.path.join("input", "tool_description", "tool_names.txt")
        valid_tools = extract_valid_tool_names(tool_name_path)
    except Exception as e:
        logger.error(f"Error loading tools or tool names: {e}")
        return None

    if not ttp_text or not tool_text:
        logger.error("Empty or invalid input. Prompt cannot be generated.")
        return None

    logger.info("Searching for tool alignment with CTI report...")
    result = run_tool_matching_prompt(ttp_text, tool_text, template_name=template_name, model=RAG_MODEL)

    evaluation = evaluate_tool_precision(result, valid_tools, logger=logger)
    report_path = os.path.join(os.path.dirname(output_path), "tool_precision_report.json")
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(evaluation, f, indent=2)
    except Exception as e:
        logger.warning(f"Could not save precision report: {e}")

    logger.info("Validating LLM output")
    result = enrich_result_with_technique_names(result, technique_map)
    result = filter_result_by_strict_tool_list(result, valid_tools)
    result = normalize_tactic_formatting(result) 

    # Save the final result to file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
    except Exception as e:
        logger.error(f"Error saving result to {output_path}: {e}")
        return None

    return result

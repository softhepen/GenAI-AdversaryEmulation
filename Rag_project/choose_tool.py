import os
import json
import re
from subprocess import run, PIPE
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

def normalize_tool_name(name):
    # Lowercase and remove dashes, spaces, and non-alphanumeric characters
    return re.sub(r"[^a-z0-9]", "", name.lower())

# Validates a single TTP entry to ensure all required fields are present
def is_valid_ttp_entry(entry):
    meta = entry.get("metadata", {})
    tactic_ids = meta.get("tactic", [])
    tactic_names = meta.get("tactic_name", [])
    tech_id = entry.get("technique")
    tech_name = meta.get("technique_name")
    desc = meta.get("description")

    # Ensure all required fields are non-empty and properly formatted
    return all([
        tactic_ids, tactic_names, tech_id,
        tech_name and str(tech_name).strip(),
        desc and str(desc).strip()
    ])

# Groups valid TTP entries by tactic and technique
def group_ttps_detailed_by_tactic(ttp_entries):
    # Nested dictionary structure: tactic → technique → descriptions
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

        # Associate each tactic ID with its name and techniques
        for tid, tname in zip(tactic_ids, tactic_names):
            tactic = grouped[tid]
            tactic["tactic_name"] = tname
            technique = tactic["techniques"][tech_id]
            technique["technique_name"] = tech_name
            technique["descriptions"].append(desc)

    return grouped

# Evaluates precision of tool predictions against a whitelist of valid tools
def evaluate_tool_precision(raw_output, valid_tools, logger=None):
    # Normalize valid tool names for comparison
    normalized_valid_tools = {
        normalize_tool_name(tool): tool for tool in valid_tools
    }

    # Extract predicted tool lines from the raw output
    tool_lines = re.findall(r"Tool:\s*(.+)", raw_output)
    predicted_tools = [
        normalize_tool_name(t.strip()) for t in tool_lines if t.strip().lower() != "no tool"
    ]

    # Compute true positives: predicted tools that are in the valid list
    tp = [normalized_valid_tools[t] for t in predicted_tools if t in normalized_valid_tools]

    # Compute false positives: predicted tools not found in the valid list
    fp = [t for t in predicted_tools if t not in normalized_valid_tools]

    # Calculate precision: TP / (TP + FP), default to 1.0 if no predictions
    precision = len(tp) / (len(tp) + len(fp)) if (tp or fp) else 1.0

    # Log precision and tool classification details
    if logger:
        logger.info(f"Tool field precision: {precision:.2f}")
        #logger.info(f"True Positives (valid tools): {tp}")
        #logger.warning(f"False Positives (invalid tools): {fp}")

    # Return evaluation summary
    return {
        "precision": precision,
        "true_positives": tp,
        "false_positives": fp,
        "total_tools": len(predicted_tools),
        "total_entries": len(tool_lines)
    }

# Converts grouped TTPs into a formatted string for prompt injection
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

# Builds a mapping from technique ID to technique name for enrichment
def build_technique_name_map(ttp_entries):
    mapping = {}
    for entry in ttp_entries:
        meta = entry.get("metadata", {})
        tech_id = entry.get("technique")
        tech_name = meta.get("technique_name")
        if tech_id and tech_name:
            mapping[tech_id] = tech_name.strip()
    return mapping

# Builds and sends the prompt to the LLM via Ollama
def run_tool_matching_prompt(ttp_text, tool_text, template_name="template_match.txt", model=RAG_MODEL):
    try:
        # Load and compile the prompt template
        prompt_path = os.path.join(os.path.dirname(__file__), TEMPLATE_FOLDER, template_name)
        template_text = load_template(prompt_path)
        compiled_prompt = template_text.replace("{{ ttp_list }}", ttp_text).replace("{{ tool_list }}", tool_text)
        #logger.info(compiled_prompt)

        # Execute the LLM with the compiled prompt
        result = run(["ollama", "run", model], input=compiled_prompt.encode("utf-8"), stdout=PIPE, stderr=PIPE)
        if result.returncode != 0:
            error_msg = result.stderr.decode("utf-8")
            logger.error(f"LLM execution failed: {error_msg}")
            return f"LLM Error: {error_msg}"

        return result.stdout.decode("utf-8").strip()

    except Exception as e:
        logger.error(f"Tool matching prompt failed: {e}")
        return ""

# Orchestrates the full matching workflow from input files to final output
def match_from_text_files(ttps_path, tools_path, output_path, template_name="template_match.txt"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    logger.info("TTP extraction from CTI report")
    # Load and process TTP entries
    try:
        with open(ttps_path, "r", encoding="utf-8") as f:
            ttp_data = json.load(f)
        grouped_ttps = group_ttps_detailed_by_tactic(ttp_data)
        ttp_text = format_detailed_ttps_for_prompt(grouped_ttps)
        technique_map = build_technique_name_map(ttp_data)

        # Save formatted TTP list for inspection
        ttp_list_path = os.path.join(os.path.dirname(output_path), "ttp_list.txt")
        with open(ttp_list_path, "w", encoding="utf-8") as f:
            f.write(ttp_text)

    except Exception as e:
        logger.error(f"Error loading or processing TTPs from {ttps_path}: {e}")
        return None

    # Load tool descriptions and valid tool names
    try:
        with open(tools_path, "r", encoding="utf-8") as f:
            tool_text = f.read().strip()

        tool_name_path = os.path.join("input", "tool_description", "tool_names.txt")
        valid_tools = extract_valid_tool_names(tool_name_path)

    except Exception as e:
        logger.error(f"Error loading tools or tool names: {e}")
        return None

    # Validate inputs before generating prompt
    if not ttp_text or not tool_text:
        logger.error("Empty or invalid input. Prompt cannot be generated.")
        return None

    logger.info("Searching for tool alignment with CTI report...")
    # Run the tool matching prompt
    result = run_tool_matching_prompt(ttp_text, tool_text, template_name=template_name)

    # Evaluate precision of the LLM output
    evaluation = evaluate_tool_precision(result, valid_tools, logger=logger)
    report_path = os.path.join(os.path.dirname(output_path), "tool_precision_report.json")
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(evaluation, f, indent=2)
    except Exception as e:
        logger.warning(f"Could not save precision report: {e}")

    # Post-process the LLM output
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

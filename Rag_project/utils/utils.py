import re
import json
from pathlib import Path
import os
import pandas as pd
from utils.logger import get_logger
import logging

# Initialize logger for this module
logger = get_logger()

# Parses a text file containing mappings between techniques and tools, extracting feasible attack actions
def parse_feasible_actions(txt_path):
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        logger.error(f"Failed to read input file: {e}")
        return []

    feasible = []
    current_tactic_id = None
    current_tactic_name = None
    current_technique_id = None
    current_technique_name = None
    current_description = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Extract tactic ID and name
        if line.startswith("- Tactic:"):
            match = re.search(r'Tactic:\s*(TA\d{4})\s+–\s+(.+)', line)
            if match:
                current_tactic_id = match.group(1)
                current_tactic_name = match.group(2).strip()
            continue

        # Extract technique ID and name
        if line.startswith("Technique:"):
            match = re.search(r'Technique:\s*(T\d{4})\s+–\s+(.+)', line)
            if match:
                current_technique_id = match.group(1)
                current_technique_name = match.group(2).strip()
            continue

        # Extract attack description
        if line.startswith("Description:"):
            match = re.search(r'Description:\s*(.+)', line)
            if match:
                current_description = match.group(1).strip()
            continue

        # Extract tool name and build the attack action object
        if line.startswith("Tool:") and current_technique_id and current_description:
            match = re.search(r'Tool:\s*(.+)', line)
            if match:
                tool_name = match.group(1).strip()
                if tool_name.lower() not in ["no tool", "none"]:
                    feasible.append({
                        "technique_id": current_technique_id,
                        "technique_name": current_technique_name,
                        "tactic_id": current_tactic_id,
                        "tactic_name": current_tactic_name,
                        "text": current_description,
                        "tool": tool_name
                    })

            # Reset technique-related fields for the next entry
            current_technique_id = None
            current_technique_name = None
            current_description = None

    if feasible:
        logger.info(f"Parsed {len(feasible)} feasible attack actions.")
    else:
        logger.error("No feasible attack actions found. Aborting.")

    return feasible

# Cleans a string to make it safe for use as a filename
def sanitize_filename(text, max_length=50):
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    text = re.sub(r'\W+', '_', text)
    return text[:max_length].strip('_')


# Retrieves the name and path of the first report file found in the input directory
def get_name_report(input_dir="input"):
    input_path = Path(input_dir)

    # Find the first subfolder
    try:
        subfolder = next(f for f in input_path.iterdir() if f.is_dir())
    except StopIteration:
        raise RuntimeError(f"No subfolder found in '{input_dir}'")

    # Find the first .json file inside the subfolder
    try:
        file = next(f for f in subfolder.iterdir() if f.is_file() and f.suffix == ".json")
    except StopIteration:
        raise RuntimeError(f"No file found in subfolder '{subfolder.name}'")

    return file.stem, str(file)

# Extracts the folder name that comes immediately after 'report' in a given path
def extract_folder_after_report(path_str):
    path = Path(path_str)
    parts = path.parts
    try:
        report_index = parts.index("report")
        return parts[report_index + 1].upper()
    except (ValueError, IndexError):
        raise RuntimeError("The path does not contain a folder after 'report'")

# Extracts valid tool names from tool_name.txt, allowing letters, numbers, hyphens, dots, and spaces
def extract_valid_tool_names(tool_name_path):
    valid_tools = set()
    try:
        with open(tool_name_path, "r", encoding="utf-8") as f:
            for line in f:
                tool = line.strip().lower()
                if re.match(r'^[a-z0-9\-\.\s]+$', tool):
                    valid_tools.add(tool)
                else:
                    logger.warning(f"Tool name rejected by pattern: '{tool}'")
    except Exception as e:
        logger.error(f"Error reading tool_name.txt: {e}")
    return valid_tools

# Adds technique names to LLM output if missing, based on technique ID mapping
def enrich_result_with_technique_names(result_text, technique_map):
    enriched_lines = []
    for line in result_text.splitlines():
        if "Technique: T" in line:
            parts = line.split("Technique: ")
            if len(parts) < 2 or "–" in parts[1]:
                enriched_lines.append(line)
                continue
            tech_id = parts[1].strip().split(" ")[0]
            tech_name = technique_map.get(tech_id, "UNKNOWN")
            enriched_lines.append(f"{parts[0]}Technique: {tech_id} – {tech_name}")
        else:
            enriched_lines.append(line)
    return "\n".join(enriched_lines)

# Normalizes formatting of Tactic lines by removing Markdown and enforcing a leading dash
def normalize_tactic_formatting(result_text):
    normalized_lines = []
    for line in result_text.splitlines():
        line = line.replace("**", "").replace("*", "").strip()
        if line.startswith("Tactic:"):
            line = f"- {line}"
        normalized_lines.append(line)
    return "\n".join(normalized_lines)

# Filters LLM output to retain only valid tools or "No tool", replacing invalid ones
def normalize_tool_name(name):
    # Remove hyphens and spaces, convert to lowercase for consistent comparison
    return re.sub(r"[\s\-]", "", name.strip().lower())

def filter_result_by_strict_tool_list(result_text, valid_tools):
    # Normalize all valid tool names for strict matching
    normalized_valid_tools = set(normalize_tool_name(tool) for tool in valid_tools)

    def is_valid_tool_name(tool_name):
        norm_name = normalize_tool_name(tool_name)
        return norm_name in normalized_valid_tools or norm_name == "notool"

    filtered_lines = []

    for line in result_text.splitlines():
        if line.lstrip().lower().startswith("tool:"):
            try:
                tool_segment = line.split("Tool:", 1)[1].split("→", 1)[0].strip()
                suffix = line.split("→", 1)[1].strip() if "→" in line else ""
                prefix = line.split("Tool:", 1)[0]

                tool_names = [t.strip() for t in tool_segment.split(",")]

                # Se più di un tool è presente, scarta la riga
                if len(tool_names) != 1 or not is_valid_tool_name(tool_names[0]):
                    logger.warning(f"Invalid or multiple tools detected: '{tool_segment}' — replacing with 'No tool'")
                    replaced_line = f"{prefix}Tool: No tool"
                    if suffix:
                        replaced_line += f" → {suffix}"
                    filtered_lines.append(replaced_line)
                else:
                    reconstructed = f"{prefix}Tool: {tool_names[0]}"
                    if suffix:
                        reconstructed += f" → {suffix}"
                    filtered_lines.append(reconstructed)

            except Exception as e:
                logger.error(f"Error parsing tool line: '{line}' — {e}")
                filtered_lines.append(line)
        else:
            filtered_lines.append(line)

    return "\n".join(filtered_lines)



# Rename the log file after execution to include report name and group
def finalize_log(logger, log_dir, reportname, group, old_name="rag.log"):
    old_path = os.path.join(log_dir, old_name)
    new_name = f"rag_{reportname}_{group}.log"
    new_path = os.path.join(log_dir, new_name)

    # Close and remove all FileHandlers from the logger
    handlers_to_close = []
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            handler.flush()
            handler.close()
            handlers_to_close.append(handler)

    for handler in handlers_to_close:
        logger.removeHandler(handler)

    # Rename the log file, overwrite if destination already exists
    if os.path.exists(old_path):
        if os.path.exists(new_path):
            os.remove(new_path)
        os.rename(old_path, new_path)




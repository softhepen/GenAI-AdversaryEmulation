from pathlib import Path
import pandas as pd
import re
import os
import evaluate
from utils.logger import get_logger

# Initialize module-level logger
logger = get_logger()

# Load chrF metric from Hugging Face's evaluate library
chrf_metric = evaluate.load("chrf")

# Extract command strings from a .txt file using regex patterns
def extract_commands_from_txt(txt_path):
    # Read all lines from the input .txt file
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    commands = []
    for i, line in enumerate(lines, 1):
        # Try to extract command enclosed in backticks
        match = re.search(r"(?:\*\*Command:\*\*|Command:)\s*`([^`]+)`", line)
        if not match:
            # Fallback: extract command without backticks
            match = re.search(r"(?:\*\*Command:\*\*|Command:)\s*(.+)", line)
        if match:
            # Clean and store the extracted command
            command = match.group(1).strip().strip("`")
            commands.append(command)
        else:
            # Log if no valid command is found on the line
            logger.debug(f"No valid command found at line {i} in {txt_path.name}")
    return commands

# Extract tool name from filename pattern like 'command_toolname_TAxxxx'
def extract_tool_from_filename(filename):
    # Use regex to extract tool name from filename
    match = re.search(r'^command_(.+?)_TA\d{4}', filename)
    # Replace underscores with spaces for readability
    return match.group(1).replace('_', ' ') if match else None

# Load and filter commands from CSV file based on tool name
def load_filtered_commands(csv_path, tool_name=None):
    try:
        # Read the CSV file with semicolon separator
        df = pd.read_csv(csv_path, sep=';', on_bad_lines='warn')
    except Exception as e:
        # Log error if CSV cannot be loaded
        logger.error(f"Error loading CSV file: {e}")
        return []

    # Check if required columns are present
    required_cols = {"APT", "COMMAND", "TOOL"}
    if not required_cols.issubset(df.columns):
        logger.error(f"Missing columns in CSV. Expected: {required_cols}, found: {df.columns.tolist()}")
        return []

    # Filter commands by tool name if provided
    filtered = df[df["TOOL"].str.lower() == tool_name.lower()] if tool_name else df

    # Return list of command strings
    return filtered["COMMAND"].dropna().astype(str).tolist()

# Compute chrF similarity score between two command strings
def compare_chrf(phrase1, phrase2):
    # Hugging Face's chrF expects raw strings, not token lists
    result = chrf_metric.compute(predictions=[phrase2], references=[phrase1])
    return round(result["score"], 3)

# Find the best matching command from a list using chrF similarity
def find_best_match(input_command, candidate_commands):
    best = {"command": None, "score": 0.0}
    for candidate in candidate_commands:
        score = compare_chrf(input_command, candidate)
        if score > best["score"]:
            best["command"] = candidate
            best["score"] = score
    return best

# Main function to process all .txt files, extract commands, match them, and optionally export results
def match_chrf(txt_folder, csv_path, export_csv=False, output_dir=None):
    # Convert folder path to Path object
    txt_dir = Path(txt_folder)
    if not txt_dir.exists():
        logger.error(f"Command folder does not exist: {txt_folder}")
        return

    results = []

    # Iterate over all .txt files in the folder
    for txt_file in txt_dir.glob("*.txt"):
        # Extract tool name from filename
        tool_name = extract_tool_from_filename(txt_file.name)
        if not tool_name:
            logger.warning(f"Could not extract tool name from filename: {txt_file.name}")
            continue

        # Load ground truth commands for the tool
        filtered_csv_commands = load_filtered_commands(csv_path, tool_name)

        # Skip tools not present in ground truth
        if not filtered_csv_commands:
            logger.info(f"Tool '{tool_name}' not found in ground truth. Skipping {txt_file.name}")
            continue

        # Extract commands from the .txt file
        txt_commands = extract_commands_from_txt(txt_file)
        if not txt_commands:
            logger.warning(f"No commands extracted from {txt_file.name}")
            continue

        # Match each extracted command against ground truth
        for cmd in txt_commands:
            match = find_best_match(cmd, filtered_csv_commands)

            matched_command = match.get("command")
            chrf_score = match.get("score")
            match_found = matched_command is not None

            # Store result for each command
            results.append({
                "file": txt_file.name,
                "tool": tool_name,
                "input_command": cmd,
                "matched_command": matched_command,
                "chrf_score": chrf_score,
                "match_found": match_found
            })

    # Export results to CSV if requested
    if export_csv and results:
        output_path = Path(output_dir or ".") / "match_results_chrf.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(results).to_csv(output_path, index=False)
        logger.info(f"Results exported to: {output_path.resolve()}")
    elif export_csv:
        logger.warning("No results to export. All tools were skipped or no matches found.")

# Extract the highest chrF score per file across multiple subfolders
def extract_max_score_chrf(
    base_dir='./output',
    output_csv='results/chrf_summary.csv',
    target_filename='match_results_chrf.csv',
    score_column='chrf_score'
):
    all_rows = []

    # Iterate over each subfolder in the base directory
    for subfolder in os.listdir(base_dir):
        subfolder_path = os.path.join(base_dir, subfolder)
        csv_path = os.path.join(subfolder_path, target_filename)

        if os.path.isdir(subfolder_path) and os.path.isfile(csv_path):
            try:
                df = pd.read_csv(csv_path)

                # Ensure required columns are present
                if 'file' in df.columns and score_column in df.columns:
                    df[score_column] = pd.to_numeric(df[score_column], errors='coerce')
                    df = df.dropna(subset=['file', score_column])

                    if df.empty:
                        continue

                    # Select row with highest score per file
                    max_idx = df.groupby('file')[score_column].idxmax()
                    df_max = df.loc[max_idx].copy()
                    df_max.insert(0, 'report', subfolder)
                    all_rows.append(df_max)
                else:
                    logger.warning(f"Missing 'file' or '{score_column}' columns in {csv_path}")
            except Exception as e:
                logger.error(f"Error reading {csv_path}: {e}")

    # Concatenate and export summary CSV
    if all_rows:
        final_df = pd.concat(all_rows, ignore_index=True)
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        final_df.to_csv(output_csv, index=False, decimal=',')
        logger.info(f"Saved summary to: {os.path.abspath(output_csv)}")
    else:
        logger.info("No valid data found in subfolders.")

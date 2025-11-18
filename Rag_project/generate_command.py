import os
from subprocess import run, PIPE

from utils.config import TEMPLATE_FOLDER, RAG_MODEL
from utils.template_handler import load_template, compile_template
from utils.logger import get_logger
from utils.rag_tool import load_tool_docs, get_tool_doc_with_fallback
#from utils.tokenizer import tokenizer
from utils.utils import parse_feasible_actions, sanitize_filename

# Initialize logger for this module
logger = get_logger()

# Loads the prompt template from file, used to generate adversary commands via LLM
def load_prompt_template(template_name):
    try:
        prompt_path = os.path.join(os.path.dirname(__file__), TEMPLATE_FOLDER, template_name)
        return load_template(prompt_path)
    except Exception as e:
        logger.error(f"Failed to load prompt template: {e}")
        return ""

# Generates an adversary command using an LLM and a compiled prompt template
def generate_command_llm(
    attack_text,
    tool_name,
    tool_doc="",
    technique_id="",
    technique_name="",
    tactic_id="",
    tactic_name="",
    model=RAG_MODEL,
    template_name="template_command.txt"
):
    try:
        template = load_prompt_template(template_name)
        if not template:
            return ""

        compiled_prompt = compile_template(template, {
            "attack_text": attack_text,
            "tool_name": tool_name,
            "tool_doc": tool_doc,
            "technique_id": technique_id,
            "technique_name": technique_name,
            "tactic_id": tactic_id,
            "tactic_name": tactic_name
        })
        #logger.info(compiled_prompt)
        logger.debug(f"Compiled prompt:\n{compiled_prompt}")

        result = run(
            ["ollama", "run", model],
            input=compiled_prompt.encode("utf-8"),
            stdout=PIPE,
            stderr=PIPE
        )

        output = result.stdout.decode("utf-8").strip()
        logger.debug(f"Raw output from model:\n{output}")
        return output

    except Exception as e:
        logger.error(f"LLM execution failed: {e}")
        return ""

# Saves the generated command to a file with a sanitized filename
def save_command(tool_name, attack_text, command_text, technique_id="", tactic_id="", output_folder="generated_commands"):
    os.makedirs(output_folder, exist_ok=True)
    safe_tool = sanitize_filename(tool_name.lower())
    safe_tech_id = sanitize_filename(technique_id)
    safe_tactic_id = sanitize_filename(tactic_id)

    filename = f"command_{safe_tool}_{safe_tactic_id}_{safe_tech_id}.txt"
    output_path = os.path.join(output_folder, filename)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(command_text)
        logger.info(f"Saved command in {output_path}")
    except Exception as e:
        logger.error(f"Failed to save command: {e}")

# Parses feasible actions, generates commands via LLM, and saves them to disk
def generate_commands_from_txt(
    input_txt_path="matched_tool_results/global_tool_mapping.txt",
    template_name="template_command.txt",
    output_folder="generated_commands",
    tool_doc_dict=None,
    vectorstore=None  
):
    matches = parse_feasible_actions(input_txt_path)
    if not matches:
        return

    if tool_doc_dict is None:
        tool_doc_dict = load_tool_docs()

    for match in matches:
        attack_text = match.get("text", "")
        tool_name = match.get("tool", "")
        technique_id = match.get("technique_id", "")
        technique_name = match.get("technique_name", "")
        tactic_id = match.get("tactic_id", "")
        tactic_name = match.get("tactic_name", "")
        if not attack_text or not tool_name:
            continue

        # Retrieves relevant documentation using semantic search (RAG)
        tool_doc = get_tool_doc_with_fallback(
            tool_name=tool_name,
            attack_text=attack_text,
            vectorstore=vectorstore,
            tool_doc_dict=tool_doc_dict
        )

        # Generates command using the LLM
        command = generate_command_llm(
            attack_text,
            tool_name,
            tool_doc=tool_doc,
            technique_id=technique_id,
            technique_name=technique_name,
            tactic_id=tactic_id,
            tactic_name=tactic_name,
            model=RAG_MODEL,
            template_name=template_name
        )

        # Saves command to disk or logs a warning if generation failed
        if command:
            save_command(tool_name, attack_text, command, technique_id=technique_id, tactic_id=tactic_id, output_folder=output_folder)
        else:
            logger.warning(f"No command generated for tool '{tool_name}' and attack: {attack_text}")

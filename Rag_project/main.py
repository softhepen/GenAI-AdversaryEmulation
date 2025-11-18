import os
from pathlib import Path
from utils.config import DOCUMENT_FOLDER
from utils.logger import get_logger
from utils.rag_tool import (
    load_tool_docs,
    prepare_chunks,
    build_vectorstore,
    load_vectorstore
)
from utils.utils import (
    get_name_report,
    extract_folder_after_report
)
from choose_tool import match_from_text_files
from generate_command import generate_commands_from_txt
from evaluation import run_evaluation_pipeline

# Disable Chroma telemetry warnings
os.environ["CHROMADB_DISABLE_TELEMETRY"] = "True"

def main():
    logger = get_logger(log_dir="logs")

    # Create output directory
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # Path for persistent vector store
    vectorstore_path = os.path.join(output_folder, "chroma_tool_docs")

    # Load or build vector store from documentation
    if os.path.exists(vectorstore_path):
        logger.info("Loading existing vectorstore from disk")
        vectorstore = load_vectorstore(persist_path=vectorstore_path)
        tool_docs = None  
    else:
        logger.info("Building vectorstore from documentation")
        tool_docs = load_tool_docs(base_folder=DOCUMENT_FOLDER)
        chunks = prepare_chunks(tool_docs)
        vectorstore = build_vectorstore(chunks, persist_path=vectorstore_path)

    # Internal tool descriptions
    tool_path = os.path.join("input", "tool_description", "extracted_tools.json")

    # Identify report name and group
    report_name, report_path = get_name_report("input/report")
    group = extract_folder_after_report(report_path)
    report_folder = os.path.join(output_folder, f"{report_name}_{group}")

    # Match tools to TTPs
    logger.info(f"Tool selection for report: {report_name}")
    match_path = os.path.join(report_folder, "tool_mapping.txt")
    match_from_text_files(
        ttps_path=report_path,
        tools_path=tool_path,
        output_path=match_path
    )

    # Generate CLI commands using RAG
    logger.info(f"Generating commands for report: {report_name}")
    commands_folder = os.path.join(report_folder, "generated_commands")
    os.makedirs(commands_folder, exist_ok=True)
    generate_commands_from_txt(
        input_txt_path=match_path,
        template_name="template_command.txt",
        output_folder=commands_folder,
        tool_doc_dict=tool_docs,      
        vectorstore=vectorstore       
    )

    # Evaluation
    if any(Path(commands_folder).glob("*.txt")):
        run_evaluation_pipeline(report_name, group, report_folder, commands_folder, logger)
    else:
        logger.warning("No commands generated. Matching skipped.")

if __name__ == "__main__":
    main()

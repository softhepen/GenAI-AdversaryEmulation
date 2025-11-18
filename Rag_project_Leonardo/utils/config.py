import os

# Base project folder
BASE_FOLDER = os.getcwd()

# Input folders
INPUT_FOLDER = os.path.join(BASE_FOLDER, "input")
DOCUMENT_FOLDER = os.path.join(INPUT_FOLDER, "doc_tools")  # Tool documentation
CTI_REPORTS_FOLDER = os.path.join(INPUT_FOLDER, "report")  # CTI reports

# Prompt templates
TEMPLATE_FOLDER = os.path.join(BASE_FOLDER, "prompts")

# Output folder
OUTPUT_FOLDER = os.path.join(BASE_FOLDER, "output")

# Model configuration
EMBEDDING_MODEL = "all-minilm:l12-v2"  # Used for semantic embedding (HuggingFace)
RAG_MODEL = "meta-llama/Meta-Llama-3-8B"  



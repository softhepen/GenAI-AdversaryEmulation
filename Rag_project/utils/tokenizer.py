import requests
from utils.logger import get_logger

logger = get_logger()

# Sends a prompt to a local LLM endpoint and logs the number of tokens used.
# Useful for estimating prompt size
def tokenizer(text):
    model = "llama3:8b-instruct-q4_K_M"
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": text, "stream": False}
        )
        data = response.json()
        token_count = data.get("eval_count", 0)
        logger.info(f"Number of token: {token_count}")
        return token_count
    except Exception as e:
        logger.error(f"Tokenizer failed: {e}")
        return -1




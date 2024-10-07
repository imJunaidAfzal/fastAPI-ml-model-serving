"""
Main FastAPI application for serving ML model with API Key authentication.

- Provides endpoints for predictions and health check.
- Includes in-memory caching and logging with daily rotation.
- API Key authentication ensures secure access.
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from dotenv import load_dotenv

from model import generate_reasoning_and_answer
from cache import Cache

load_dotenv()

# Create logs directory if it doesn't exist
LOG_DIRECTORY = "logs"
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

# Set up logging configuration with daily rotation and 30 days backup
log_file_path = os.path.join(LOG_DIRECTORY, "app.log")
logging.basicConfig(level=logging.INFO)

# Create TimedRotatingFileHandler for logging
handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=30)
handler.suffix = "%Y-%m-%d"
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Get the root logger and add the handler
logger = logging.getLogger()
logger.addHandler(handler)

app = FastAPI()

# Initialize cache with a time-to-live (TTL) of 500 seconds
cache = Cache(ttl=500)

# API Key authentication setup
API_KEY = os.getenv("AUTH_KEY")
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)

def verify_api_key(api_key: str = Depends(api_key_header)):
    """
    Verify the provided API key in the request header.
    Raises an HTTPException if the key is invalid.

    Args:
        api_key (str): The API key provided in the request.

    Returns:
        str: Returns the API key if valid.
    """
    if api_key != API_KEY:
        logger.warning(f"Unauthorized access attempt with API key: {api_key}")
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

class InputText(BaseModel):
    text: str

@app.post("/predict/")
async def predict(user_input: InputText, api_key: str = Depends(verify_api_key)):
    """
    Handle prediction requests by checking the cache first,
    and if not available, perform model inference.
    API Key authentication is required.

    Args:
        user_input (InputText): Input text to be processed by the model.

    Returns:
        dict: Generated answer from the model or cached value.
    """
    # Check if the result is in the cache
    cached_result = cache.get(user_input.text)
    if cached_result:
        logger.info(f"Cache hit for request: {user_input.text}")
        return {"result": cached_result}

    try:
        result = generate_reasoning_and_answer(user_input.text)
        logger.info(
            f"Successfully generated answer for request: {user_input.text}"
        )
    except Exception as exp:
        logger.error(
            f"Error while generating answer.\nRequest: {user_input.text}\nError: {exp}"
        )
        result = "Something went wrong. Please try again in a while."

    # Store result in cache
    cache.set(user_input.text, result)

    return {"result": result}

@app.get("/health/")
async def health(api_key: str = Depends(verify_api_key)):
    """
    Health check endpoint to verify the API is running.
    API Key authentication is required.

    Returns:
        dict: Status of the service.
    """
    logger.info("Health check endpoint called.")
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

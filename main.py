import uvicorn
from fastapi import FastAPI

from logger_config import setup_logger

logger = setup_logger(logger_name='fastapi_logger')

app = FastAPI()
logger.info("Main module initialized")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

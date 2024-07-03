import uvicorn
from fastapi import FastAPI

from app.adapters.controllers.users import user_router
from app.config.logger_config import setup_logger

logger = setup_logger(logger_name='fastapi_logger')

app = FastAPI()
logger.info("Main module initialized")

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)

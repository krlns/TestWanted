import logging
from fastapi import FastAPI
from database import engine, Base
from endpoints import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/transactions", tags=["transactions"])


@app.on_event("startup")
async def startup_event():
    logger.info("Transaction service starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Transaction service shutting down...")

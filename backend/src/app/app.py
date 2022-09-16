"""Startup of FastAPI application"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """give a Hello World message"""
    return {"message": "Hello World"}

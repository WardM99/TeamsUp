"""Startup of FastAPI application"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routers import games_router


app = FastAPI(
    title="TeamsUp",
    version="0.0.1"
)


# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routes
app.include_router(games_router)

@app.get("/")
async def root():
    """give a Hello World message"""
    return {"message": "Hello World"}

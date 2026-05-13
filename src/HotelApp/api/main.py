"""
FastAPI application for HOT TEL - Hotel Management System.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..core.config import settings
from .routers import users_router, rooms_router, user_history_router, hotel_router

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="API para gestión de reservas y administración del hotel HOT TEL",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(user_history_router)
app.include_router(hotel_router)


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Welcome to HOT TEL API",
        "version": settings.api_version,
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

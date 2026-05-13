#!/usr/bin/env python
"""
Script to start the FastAPI server for HOT TEL.
Usage: python run_api.py
"""

import uvicorn
from src.HotelApp.api import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

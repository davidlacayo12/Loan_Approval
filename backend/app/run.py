# Execution Script using Uvicorn to serve FastAPI app

import uvicorn

__author__ = "David Lacayo"

# For dev, this is at: http://127.0.0.1:8000/docs


def serve():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
    )

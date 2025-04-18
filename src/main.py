from datetime import datetime

import uvicorn
from fastapi import FastAPI

from settings import settings

app = FastAPI()


@app.get("/api/health")
async def get_health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.api_host,
                port=settings.api_port,
                reload=settings.debug)

# app/main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import httpx
import logging

from .config import settings

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("stage0")

app = FastAPI(title="Stage0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def utc_iso_now() -> str:
    """Return current UTC time in ISO 8601 format with 'Z' suffix."""
    now = datetime.now(timezone.utc)
    iso = now.isoformat(timespec="milliseconds")
    return iso.replace("+00:00", "Z")

@app.get("/")
async def root():
    return {"message": "Welcome to Stage0!"}

@app.get("/me")
async def get_profile():
    user_data = {
        "email": settings.EMAIL,
        "name": settings.NAME,
        "stack": settings.STACK
    }

    cat_fact = None
    try:
        timeout = httpx.Timeout(settings.EXTERNAL_TIMEOUT)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(settings.CATFACT_URL)
            if response.status_code == 200:
                data = response.json()
                cat_fact = data.get("fact")
            else:
                logger.warning(f"Cat Facts API returned {response.status_code}")
    except httpx.TimeoutException:
        logger.error("Cat Facts API request timed out.")
    except httpx.RequestError as e:
        logger.error(f"Network error contacting Cat Facts API: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")

    if not cat_fact:
        cat_fact = "Could not fetch a cat fact right now — please try again later."

    payload = {
        "status": "success",
        "user": user_data,
        "timestamp": utc_iso_now(),
        "fact": cat_fact
    }

    return JSONResponse(content=payload, status_code=200)

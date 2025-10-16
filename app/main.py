# app/main.py
from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import httpx
import logging
import json
from .config import settings

# from fastapi import FastAPI, Request
# from slowapi import Limiter
# from fastapi.responses import JSONResponse



limiter = Limiter(key_func=get_remote_address)

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("stage0")

app = FastAPI(title="Stage0")
app.state.limiter = limiter

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )

def utc_iso_now() -> str:
    """Return current UTC time in ISO 8601 format with 'Z' suffix."""
    now = datetime.now(timezone.utc)
    iso = now.isoformat(timespec="milliseconds")
    return iso.replace("+00:00", "Z")

@app.get("/")
async def root():
    return RedirectResponse(url="/me")

@app.get("/me")
@limiter.limit("5/minute")
async def get_profile(request: Request):
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
        "fact": cat_fact,
        "timestamp": utc_iso_now()
    }

    return Response(
        content=json.dumps(payload, indent=4),
        media_type="application/json",  status_code=200
    )
    # return JSONResponse(content=payload, media_type="application/json", indent=4, status_code=200) # type: ignore

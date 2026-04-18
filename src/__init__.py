import os
import logging
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from src.auth import authenticate
from src.endpoints import router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    api_key = os.getenv("BRIGHTDATA_API_KEY")
    if api_key:
        try:
            from brightdata import BrightDataClient
            client = BrightDataClient(token=api_key, timeout=120)
            await client.__aenter__()
            app.state.sdk_client = client
            logger.info("BrightData SDK session initialized")
        except ImportError:
            logger.error("brightdata-sdk not installed — BrightData scraping unavailable")
            app.state.sdk_client = None
        except Exception as e:
            logger.error(f"Failed to initialize BrightData SDK: {e}")
            app.state.sdk_client = None
    else:
        logger.warning("BRIGHTDATA_API_KEY not set — BrightData scraping unavailable")
        app.state.sdk_client = None

    yield

    if getattr(app.state, "sdk_client", None):
        try:
            await app.state.sdk_client.__aexit__(None, None, None)
            logger.info("BrightData SDK session closed")
        except Exception as e:
            logger.debug(f"Error closing BrightData SDK session: {e}")


def create_app():

    app = FastAPI(dependencies=[Depends(authenticate)], lifespan=lifespan)

    @app.get("/")
    async def root():
        return PlainTextResponse("Navigate to '/docs' for testing", status_code=200)

    app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

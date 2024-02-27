from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from src.auth import authenticate
from src.endpoints import router


def create_app():

    app = FastAPI(dependencies=[Depends(authenticate)])

    @app.get("/")
    async def root():
        return PlainTextResponse("Navigate to '/docs' for testing", status_code=200)
    
    app.include_router(router)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # allow all origins
        allow_credentials=True, # allow cookies
        allow_methods=["*"], # allow all methods
        allow_headers=["*"], # allow all headers
    )

    return app
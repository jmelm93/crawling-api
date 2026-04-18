# CLAUDE.md

Web crawling microservice — FastAPI + BrightData Web Unlocker SDK. Deployed on Google Cloud Run.

## Tech Stack

- **Python 3.11**, FastAPI, aiohttp, uvicorn
- **BrightData SDK v2.x** (`brightdata-sdk==2.1.1`) for bot bypass and JS rendering
- Docker (`python:3.11-slim`), Google Cloud Run (1Gi/1CPU)

## How It Works

Single endpoint: `POST /crawl` with `{url, render_js}` → `{url, content, status_code}`

- `render_js=False`: aiohttp fetches directly (free). Falls back to BrightData SDK on failure or non-2xx.
- `render_js=True`: BrightData SDK handles JS rendering server-side.

All endpoints require HTTP Basic Auth (`API_USERNAME`/`API_PASSWORD`).

## Architecture

- `main.py` — Entry point, runs uvicorn
- `src/__init__.py` — App factory (`create_app()`), SDK lifespan (init on startup, close on shutdown), CORS
- `src/endpoints.py` — `/crawl` route, passes `request.app.state.sdk_client` to crawl logic
- `src/crawl_page.py` — Core logic: `fetch_with_aiohttp()`, `fetch_with_sdk()`, `crawl_page()`
- `src/auth.py` — HTTP Basic Auth via env vars
- `uvicorn_config.py` — Server config (workers = CPU count, port from `PORT` env var)

## Environment Variables

```
BRIGHTDATA_API_KEY=...       # BrightData Web Unlocker SDK (required for SDK scraping)
API_USERNAME=...             # HTTP Basic Auth
API_PASSWORD=...             # HTTP Basic Auth
GOOGLE_CLOUD_PROJECT_ID=...  # Used by deploy.sh for GCR
TEST_URL=...                 # Used by tests
```

## Commands

```bash
python main.py                    # Run locally
pytest src/test_endpoints.py -v   # Run tests (hits real URLs + BrightData)
./deploy.sh                       # Build + deploy to Cloud Run
./deploy_local.sh                 # Build + run in Docker locally
```

## Key Patterns

- **SDK lifecycle**: Managed via FastAPI async lifespan in `src/__init__.py`. Client stored on `app.state.sdk_client`. Endpoints access it via `request.app.state`.
- **Graceful degradation**: If `BRIGHTDATA_API_KEY` is missing or SDK fails to init, `sdk_client` is `None` — `render_js=True` returns `status_code: 503`, `render_js=False` still works via aiohttp.
- **Tests require context manager**: `TestClient` must be used with `with` statement to trigger the lifespan (see `test_endpoints.py` fixture).

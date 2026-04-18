# FastAPI Web Crawler (Docker/Google Cloud Run Deployment Ready)

This FastAPI application provides an API endpoint to crawl web pages with the option to render JavaScript. It's designed to be deployed in a Docker container, making it scalable and easy to deploy on cloud platforms like Google Cloud Run.

Uses the BrightData Web Unlocker SDK for JavaScript rendering (server-side) and bot bypass, with aiohttp for direct static page fetching.

## How It Works

- `render_js=False`: Fetches the page directly with aiohttp (free, fast). Falls back to BrightData SDK if the direct request fails or returns a non-2xx status.
- `render_js=True`: Uses the BrightData SDK directly, which handles JavaScript rendering server-side along with bot detection bypass.

## Local Development
1. Clone the repo
2. Create a Virtual Environment
3. Install dependencies: `pip install -r requirements.txt`
4. Create `.env` file:
```
BRIGHTDATA_API_KEY=your_brightdata_api_key
API_USERNAME=api_username
API_PASSWORD=api_password
TEST_URL=your_test_url
GOOGLE_CLOUD_PROJECT_ID=your_google_cloud_project_id
```
5. Run the app with `python main.py`
6. Navigate to `http://127.0.0.1:8000/docs` for testing

## Deployment
1. Ensure you have gcloud sdk on your computer (https://cloud.google.com/sdk/docs/install)
2. Run `gcloud auth login` and login to whatever email you want to deploy to
3. Set the project with `gcloud config set project {{ PROJECT NAME }}`
4. Run `./deploy.sh` to deploy

## Files in Application
- `src/__init__.py`: The main FastAPI application factory with BrightData SDK lifecycle management.
- `src/endpoints.py`: The endpoint definition for the API.
- `src/crawl_page.py`: Contains the crawling logic using aiohttp (direct) and BrightData SDK (fallback/JS rendering).
- `src/auth.py`: HTTP Basic Authentication.
- `Dockerfile`: Instructions for Docker on how to build the application image.
- `.env`: Environment variables (not committed to git).
- `deploy.sh`: Bash script to deploy to Google Cloud Run.
- `deploy_local.sh`: Bash script to deploy locally via Docker.

## Features
- `Web Crawling`: Supports crawling both JavaScript-rendered pages and plain HTML content.
- `BrightData SDK`: Uses the Web Unlocker SDK for bot bypass, CAPTCHA handling, and server-side JS rendering.
- `Smart Fallback`: Direct aiohttp fetch first (free), BrightData SDK fallback on failure.
- `Dockerization`: Packaged with Docker for easy deployment and scaling.
- `Cloud Deployment Ready`: Easily deployable to Google Cloud Run.

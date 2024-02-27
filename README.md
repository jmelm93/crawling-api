# FastAPI Web Crawler (Docker/Google Cloud Run Deployment Ready)

This FastAPI application provides an API endpoint to crawl web pages with the option to render JavaScript. It's designed to be deployed in a Docker container, making it scalable and easy to deploy on cloud platforms like Google Cloud Run.

This application uses Playwright for JavaScript rendering and aiohttp for static page rendering. Both are setup for async crawling to ensure efficiency.

## Proxy Configuration
- There are many options available. I personally used https://brightdata.com/.

## Local Development
1. Clone the repo
2. Create a Virtual Environment
3. Install dependencies
4. Create `.env` file with the below dependencies.
```
PROXY_HOST=your_proxy_host
PROXY_USERNAME=your_proxy_username
PROXY_PASSWORD=your_proxy_password
API_USERNAME=api_username
API_PASSWORD=api_password
TEST_URL=your_test_url
GOOGLE_CLOUD_PROJECT_ID=you_google_cloud_project_id
```
5. Run the app with `uvicorn main:app`
6. Navigate to `http://127.0.0.1:8000/docs` for testing 

## Deployment
1. Ensure you have gcloud sdk on your computer (https://cloud.google.com/sdk/docs/install)
2. Run `gcloud auth login` and login to whatever email you want to deploy to
3. Set the project with `gcloud config set project {{ PROJECT NAME }}`
4. Run `./deploy.sh` to deploy

## Files in Application
- `src/__init__.py`: The main FastAPI application to instantiate the extensions.
- `src/endpoints.py`: The endpoint definition for th API.
- `src/crawl_page.py`: Contains the logic for the web crawler, supporting both JavaScript-rendered and plain HTML pages.
- `Dockerfile`: Instructions for Docker on how to build the application image.
- `.env`: A file for storing environment variables like proxy settings. (This file will not exist until you create it following the setup instructions.)
- `deploy.sh`: Bash script to deploy the final application to Google Cloud Run.
- `deploy_local.sh`: Bash script to deploy to local dockerized application.

## Features
- `Web Crawling`: Supports crawling both JavaScript-rendered pages and plain HTML content.
- `Proxy Support`: Can use proxy settings defined in .env file for web crawling, useful for bypassing IP-based rate limiting or geofencing.
- `Dockerization`: Packaged with Docker for easy deployment and scaling.
- `Cloud Deployment Ready`: Easily deployable to Google Cloud Run or other cloud platforms that support Docker.
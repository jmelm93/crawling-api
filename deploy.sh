#!/bin/bash

APP_NAME="crawling-api"                          # name of the application
CURRENT_DATE_TIME=$(date +%Y-%m-%d-%H-%M)        # e.g. 2020-01-01-12-00
BUILD_TAG="build_${CURRENT_DATE_TIME}"           # Build Tag: e.g., build_2022-07-10-04-01
REGION="us-central1"                             # Google Cloud region
TIMEOUT="60m"                                    # Timeout for the deployment - timeout max for cloudrun is 60 minutes
MEMORY="1Gi"                                     # Memory for the deployment (reduced: no more Playwright/Chromium)
CPU="1"                                          # CPU for the deployment (reduced: no more browser rendering)


# Load environment variables from .env file.
if [ -f .env ]; then
    export $(cat .env | xargs)
fi


echo '************************************************************************************'
echo "Starting $APP_NAME as `whoami`"
echo '************************************************************************************'


echo "--------------------------------------------------------------------------------"
echo "Building the Docker image to push to Google Container Registry ..."
echo "--------------------------------------------------------------------------------"
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT_ID}/${APP_NAME}:${BUILD_TAG} .

if [ $? -eq 0 ]; then # if build is successful, then push the image to gcr.io
    echo "--------------------------------------------------------------------------------"
    echo "Build succeeded. Deploying the image to Cloud Run ..."
    echo "--------------------------------------------------------------------------------"

    gcloud run deploy ${APP_NAME} \
        --platform managed \
        --image=gcr.io/${GOOGLE_CLOUD_PROJECT_ID}/${APP_NAME}:${BUILD_TAG} \
        --region=${REGION} \
        --timeout=${TIMEOUT} \
        --memory=${MEMORY} \
        --cpu=${CPU} \
        --set-env-vars BRIGHTDATA_API_KEY=${BRIGHTDATA_API_KEY},API_USERNAME=${API_USERNAME},API_PASSWORD=${API_PASSWORD}

else # if build fails, then exit
    echo "--------------------------------------------------------------------------------"
    echo "Build failed. Exiting ..."
    echo "--------------------------------------------------------------------------------"
    exit 1
fi

    echo "--------------------------------------------------------------------------------"
    echo "Done."

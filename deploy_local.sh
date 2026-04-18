# Load environment variables from .env file.
if [ -f .env ]; then
    export $(cat .env | xargs)
fi


# Build docker image
docker build -t crawling-api .


# Stop anything running on port 8080
docker stop $(docker ps -q --filter "ancestor=crawling-api") || true

# Launch in background
docker run -d -p 8080:8080 \
  -e BRIGHTDATA_API_KEY=${BRIGHTDATA_API_KEY} \
  -e API_USERNAME=${API_USERNAME} \
  -e API_PASSWORD=${API_PASSWORD} \
  crawling-api

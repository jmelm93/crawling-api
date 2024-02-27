# Load environment variables from .env file. 
if [ -f .env ]; then
    export $(cat .env | xargs)
fi


# Build docker image with build arguments
docker build -t crawling-api \
  --build-arg PROXY_HOST=${PROXY_HOST} \
  --build-arg PROXY_USERNAME=${PROXY_USERNAME} \
  --build-arg PROXY_PASSWORD=${PROXY_PASSWORD} \
  --build-arg API_USERNAME=${API_USERNAME} \
  --build-arg API_PASSWORD=${API_PASSWORD} .
  

# Stop anything running on port 8080
docker stop $(docker ps -q --filter "ancestor=crawling-api") || true

# Launch in background
docker run -d -p 8080:8080 \
  -e PROXY_HOST=${PROXY_HOST} \
  -e PROXY_USERNAME=${PROXY_USERNAME} \
  -e PROXY_PASSWORD=${PROXY_PASSWORD} \
  -e API_USERNAME=${API_USERNAME} \
  -e API_PASSWORD=${API_PASSWORD} \
  crawling-api

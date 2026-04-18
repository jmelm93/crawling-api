FROM python:3.11-slim

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add app
COPY . .

# Run uvicorn when the container launches
CMD ["python3", "main.py"]

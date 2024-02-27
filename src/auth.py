import os
import logging
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

load_dotenv()

security = HTTPBasic()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def authenticate(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv('API_USERNAME')
    correct_password = os.getenv('API_PASSWORD')
    if not (credentials.username == correct_username and credentials.password == correct_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return True


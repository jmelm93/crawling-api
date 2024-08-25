from src import create_app
from uvicorn_config import config
import uvicorn

app = create_app()  

if __name__ == '__main__':
    uvicorn.run("main:app", **config)

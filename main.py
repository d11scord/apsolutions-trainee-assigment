import uvicorn
from fastapi import FastAPI

from src.app import create_app

app: FastAPI = create_app()


if __name__ == '__main__':
    uvicorn.run("main:app", port=80, host='127.0.0.1')

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="ESearch Engine", openapi_url="/docs.json")


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run("main:app", port=80, host='127.0.0.1')

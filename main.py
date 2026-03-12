from fastapi import FastAPI
from application.routers import router as api_router
from application.config.container import Container


app = FastAPI()
container = Container()

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}

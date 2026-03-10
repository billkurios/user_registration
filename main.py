from fastapi import FastAPI
from application.routers.user_router import router as user_router
from application.config.container import Container

app = FastAPI()
container = Container()

app.include_router(user_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}

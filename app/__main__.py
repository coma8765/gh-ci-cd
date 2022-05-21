import os

from fastapi import FastAPI

from .routes import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    # noinspection PyTypeChecker
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT", 8000)))

import os

from app import app
from .routes import router

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    # noinspection PyTypeChecker
    uvicorn.run(
        "app.__main__:app",
        host=os.getenv("HOST") or "0.0.0.0",
        port=int(os.getenv("PORT") or 8000),
        reload=bool(os.getenv("DEBUG", False)),
    )

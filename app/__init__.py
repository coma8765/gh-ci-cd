from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from . import db
from .views.routes import add_exception_handlers, router

app = FastAPI()
app.include_router(router)
app.on_event("startup")(db.startup)
add_exception_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

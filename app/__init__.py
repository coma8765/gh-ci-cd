from fastapi import FastAPI
from pydantic import BaseConfig

from . import db
from .views.routes import add_exception_handlers, router

app = FastAPI()
app.include_router(router)
app.on_event("startup")(db.startup)
add_exception_handlers(app)

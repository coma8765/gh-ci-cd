from fastapi import APIRouter

from .auth_router import router as auth_router
from .exc import add_exception_handlers

router = APIRouter()
router.include_router(auth_router)


@router.get("/")
def available():
    return {"status": "success"}


__all__ = ["router", "add_exception_handlers"]

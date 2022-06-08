from fastapi import APIRouter

from .auth_router import router as auth_router
from .files_router import router as files_router
from .exc import add_exception_handlers

router = APIRouter()
router.include_router(auth_router)
router.include_router(files_router)


@router.get("/", tags=["available"])
def available():
    return {"status": "success"}


__all__ = ["router", "add_exception_handlers"]

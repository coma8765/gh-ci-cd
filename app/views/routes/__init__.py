from fastapi import APIRouter

from .auth_router import router as auth_router

router = APIRouter()
router.include_router(auth_router)


@router.get("/")
def available():
    return {"status": "success"}

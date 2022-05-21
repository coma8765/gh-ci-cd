from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def available():
    return {"status": "success"}

from fastapi import APIRouter, HTTPException, Response, status

from .schema import *
from ....controllers import auth as c

router = APIRouter(tags=["auth"])


@router.post("/signup", status_code=201, response_model=c.UserShort)
async def signup(data: c.UserRef, response: Response):
    response.headers["Cache-Control"] = "no-store"

    try:
        return await c.signup(data)
    except c.UserAlreadyExists as e:
        raise HTTPException(status_code=400, detail=len(e.args) and e.args[0] or "")


@router.post("/signin", response_model=c.Token)
async def signin(data: c.UserRef, response: Response):
    response.headers["Cache-Control"] = "no-store"

    try:
        return c.create_auth_token((await c.signin(data)).id)

    except c.SignInWrong as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=len(e.args) and e.args[0] or "Some error",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get(
    "/check_email_exists",
    response_model=EmailExists,
)
async def check_email_exists(email: c.EmailStr, response: Response):
    response.headers["Cache-Control"] = "public, max-age=360"

    return EmailExists(exists=await c.check_email_exists(email))

from fastapi import APIRouter, HTTPException, UploadFile
from starlette import status
from starlette.responses import Response

from ....controllers.files import *
from ....controllers.files.slides import *

router = APIRouter(prefix="/files", tags=["files"])


@router.post("", response_model=File)
async def upload_route(file: UploadFile):
    return await upload(FileUpload(
        filename=file.filename,
        read=file.read
    ))


@router.get("", response_model=list[File])
async def list_files_route(response: Response):
    response.headers["Cache-Control"] = "public, must-revalidate"
    return await list_files()


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(file_id: int):
    try:
        await remove_file(file_id)
    except FileNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
            headers={"Cache-Control": "public, max-age=360"}
        )


@router.get(
    "/slides",
    tags=["slides"],
    response_model=list[Slide],
    responses={
        400: {"description": "File is damaged"}
    }
)
async def slides_info_route(file_id: int):
    try:
        return await get_slides_info(file_id)
    except FileNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    except BadFile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is damaged"
        )

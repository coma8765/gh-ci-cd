import mimetypes
from typing import Callable, Coroutine

from pydantic import BaseModel, Field, constr, validator

from app.controllers.files.exc import BadFile
from app.controllers.files.slides import get_slides_info_by_filename

mimetypes.init()


class FileBase(BaseModel):
    filename: constr(max_length=100) = ""

    @property
    def mimetype(self) -> str | None:
        return mimetypes.types_map.get(self.extension, None)

    @property
    def extension(self) -> str:
        return "." + self.filename.split(".")[-1]


class FileUpload(FileBase):
    read: Callable[[], Coroutine[None, None, bytes]]


class FileTypeSlides(BaseModel):
    count_slides: int


class FileTypeNotImplemented(BaseModel):
    pass


class File(FileBase):
    id: int
    type_addons: FileTypeNotImplemented | FileTypeSlides = Field(
        FileTypeNotImplemented(), alias="type_addons"
    )

    @validator("type_addons", always=True)
    def set_type_addons(cls, v, values, **kwargs):
        if values["filename"].endswith(".ppt") or values["filename"].endswith(".pptx"):
            try:
                slides = get_slides_info_by_filename(
                    values["id"], "." + values["filename"].split(".")[-1]
                )

                return FileTypeSlides(count_slides=len(slides))
            except BadFile:
                pass
        return FileTypeNotImplemented()

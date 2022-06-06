import mimetypes
from typing import Callable, Coroutine

from pydantic import BaseModel, constr

mimetypes.init()


class FileBase(BaseModel):
    filename: constr(max_length=100) = ""

    @property
    def mimetype(self) -> str | None:
        return mimetypes.types_map.get(
            self.extension,
            None
        )

    @property
    def extension(self) -> str:
        return "." + self.filename.split(".")[-1]


class FileUpload(FileBase):
    read: Callable[[], Coroutine[None, None, bytes]]


class File(FileBase):
    id: int

import aiofiles

from .exc import FileNotFound
from .schema import *
from ...db import Session
from ...dependencies import session
from ...settings import STORAGE


@session
async def upload(file: FileUpload, db: Session = None) -> File:
    id_ = await db.fetchval(
        "INSERT INTO files (filename, mimetype) VALUES ($1, $2) "
        "LIMIT 100 RETURNING id",
        file.filename,
        file.mimetype,
    )

    async with aiofiles.open(
        STORAGE / f"{id_}{file.extension or '.unknown'}", "wb"
    ) as f:
        await f.write(await file.read())

    return File(
        **file.dict(exclude={"read"}),
        id=id_,
    )


@session
async def list_files(db: Session = None) -> list[File]:
    files = await db.fetch(
        "SELECT id, filename, mimetype FROM files ORDER BY id DESC LIMIT 100"
    )

    return list(map(lambda x: File(id=x["id"], filename=x["filename"]), files))


@session
async def remove_file(file_id: int, db: Session):
    f = await db.fetchrow("SELECT id FROM files WHERE id=$1", file_id)
    if f is None:
        raise FileNotFound

    await db.fetchval("DELETE FROM files WHERE id=$1", file_id)

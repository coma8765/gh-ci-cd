from typing import List

import pptx

from .schemas import *
from .. import FileBase
from ..exc import FileNotFound
from ....db import Session
from ....dependencies import session
from ....settings import STORAGE, STORAGE_PRESENTATION_IMAGES


@session
async def get_slides_info(file_id: int, db: Session) -> List[Slide]:
    filename: Optional[str] = (await db.fetchrow(
        "SELECT filename FROM files WHERE id=$1 AND filename LIKE '%.ppt%'",
        file_id
    )).get("filename", None)

    if filename is None:
        raise FileNotFound

    p: pptx.Presentation() = pptx.Presentation(
        STORAGE / f"{file_id}{FileBase(filename=filename).extension}",
    )

    return list(map(
        lambda x: Slide(
            image_path=f"{STORAGE_PRESENTATION_IMAGES}/{file_id}-"
                       f"{x[0] > 9 and x[0] or f'0{x[0]}'}.jpg",
            comment=
            x[1].has_notes_slide and
            x[1].notes_slide.notes_text_frame.text.strip() or ""
        ),
        enumerate(p.slides)
    ))

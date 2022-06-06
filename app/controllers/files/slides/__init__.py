from typing import Any, Dict, List
from zipfile import BadZipFile

import pptx

from .schemas import *
from .. import FileBase
from ..exc import BadFile, FileNotFound
from ....db import Session
from ....dependencies import session
from ....settings import STORAGE, STORAGE_PRESENTATION_IMAGES


@session
async def get_slides_info(file_id: int, db: Session) -> List[Slide]:
    r: Optional[Dict[str, Any]] = await db.fetchrow(
        "SELECT filename FROM files WHERE id=$1 AND filename LIKE '%.ppt%'",
        file_id
    )

    if r is None:
        raise FileNotFound

    try:
        p: pptx.Presentation() = pptx.Presentation(
            STORAGE / f"{file_id}{FileBase(filename=r['filename']).extension}",
        )
    except BadZipFile or ValueError or TypeError:
        raise BadFile

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

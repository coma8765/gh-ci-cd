from typing import Optional

from pydantic import BaseModel


class Slide(BaseModel):
    image_path: str
    comment: Optional[str]


class Slides(BaseModel):
    slides: Slide

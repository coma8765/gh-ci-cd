import os
import pathlib

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALG = "HS256"

STORAGE = pathlib.Path(os.getenv("STORAGE", "/tmp"))
print(STORAGE)
STORAGE_PRESENTATION_IMAGES = \
    STORAGE / os.getenv("STORAGE_PRESENTATION_IMAGES", "slides")

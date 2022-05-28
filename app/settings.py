import os

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALG = "HS256"

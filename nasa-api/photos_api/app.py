from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from photos_api.photo_cache import PhotoCache

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "This is the space hacks api.  Space photos available at /v1/photo"
    }


@app.get("/v1/photo")
async def get_photo():
    cached_photos.check_cache()
    return cached_photos.random()


# Set up requirements
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cached_photos = PhotoCache()

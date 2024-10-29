"""Serve a basic photo grab endpoint pulling from a cache of NASA photos"""

import random
from typing import List

import requests
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Pydantic handler for environment secrets"""

    nasa_photos_api_url: str
    nasa_api_key: str

    class Config:
        env_file = "api.env"


class NasaApiRequest(BaseModel):
    """Model containing the allowed parameters for a request to the NASA photos endpoint"""

    count: int = 10
    api_key: str = None


class NasaApiResponse(BaseModel):
    """Model containing the expected response from the NASA photos endpoint"""

    copyright: str = None
    date: str = None
    explanation: str
    hdurl: str = None
    title: str
    url: str


class PhotoCache:

    def __init__(self):
        """Initialize the cache with 10 photos"""
        self.settings = Settings()
        self.cache = self.fetch_nasa_photos()

    def random(self):
        """Grab a random photo from the cache and refill if necessary"""
        photo = random.choice(self.cache)
        self.cache.remove(photo)

        return photo

    def check_cache(self) -> bool:
        """If only 2 photos are left, fetch 10 new ones to refill the cache"""
        if len(self.cache) <= 2:
            self.cache.extend(self.fetch_nasa_photos())

        return True

    def fetch_nasa_photos(self) -> List[dict]:
        """Grab 10 photos from the NASA API at once to cache"""
        # Validate parameters against API expectation and add API key
        # TODO: We're going to expand this model to allow passing parameters from: the app UI -> our API -> external API
        validated_params = NasaApiRequest()
        validated_params.api_key = self.settings.nasa_api_key

        # Make the request and handle any status errors
        response = requests.get(
            self.settings.nasa_photos_api_url, params=validated_params.dict()
        )
        response.raise_for_status()

        # Validate the response against the model expectation
        validated_response = [NasaApiResponse(**r) for r in response.json()]

        return validated_response

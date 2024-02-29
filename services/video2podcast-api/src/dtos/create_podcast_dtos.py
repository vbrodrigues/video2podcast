from pydantic import BaseModel
from typing import Optional


class CreatePodcastDTO(BaseModel):
    video_url: str
    person1: str
    person2: str
    skip_podcast: bool


class CreatePodcastResponseDTO(BaseModel):
    success: bool
    message: Optional[str]


class PublishCreatePodcast(CreatePodcastDTO):
    video_id: str
    user_id: str
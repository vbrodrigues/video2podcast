import uuid
import os
from fastapi import Depends, FastAPI
from dependencies.google import pubsub_publisher, storage_client
from dtos.create_podcast_dtos import CreatePodcastDTO, CreatePodcastResponseDTO, PublishCreatePodcast


app = FastAPI()


@app.post('/podcast')
def video2podcast(request: CreatePodcastDTO, publisher = Depends(pubsub_publisher)) -> CreatePodcastResponseDTO:
    try:

        video_id = str(uuid.uuid4())
        temp_user_id = str(uuid.uuid4())
        # TODO: Salvar metadata no Firestore com status PENDING
        topic_name = 'projects/{project_id}/topics/{topic}'.format(
            project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
            topic='create-podcast',  # Set this to something appropriate.
        )
        publish_data = PublishCreatePodcast(**{**request.model_dump(), 'video_id': video_id, 'user_id': temp_user_id})
        print('Publishing', publish_data.model_dump_json().encode('utf-8'))
        future = publisher.publish(topic_name, data=publish_data.model_dump_json().encode('utf-8'))
        print('Published:', future.result())

        return CreatePodcastResponseDTO(success=True, message='Podcast creation started')

    except Exception as e:
        return CreatePodcastResponseDTO(success=False, message=str(e))
from google.cloud import pubsub_v1
from google.cloud.storage import Client


publisher = pubsub_v1.PublisherClient()
storage = Client()


def pubsub_publisher():
    return publisher


def storage_client():
    return storage

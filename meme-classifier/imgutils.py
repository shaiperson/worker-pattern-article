import io
import requests
from runnerlib import exceptions


def image_url_to_bytes(url):
    response = requests.get(url)
    if not response.ok:
        raise exceptions.RequestError('', response)
    return io.BytesIO(response.content)

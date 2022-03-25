import logging
import traceback

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import classifier
from settings import settings
import exceptions

logger = logging.getLogger('Server')


class ClassificationRequest(BaseModel):
    image_url: str


class ClassificationResponse(BaseModel):
    label: str
    score: float


app = FastAPI()


@app.post("/", status_code=200)
async def create_item(request: ClassificationRequest):
    try:
        logger.info('Running classifier on URL'.format(request.image_url))
        label, score = classifier.run_on_url(request.image_url)
        return ClassificationResponse(label=label, score=score)

    except exceptions.RequestError as e:
        raise HTTPException(status_code=400, detail=f'Error fetching request image, received {e.response.status_code}')

    except Exception as e:
        error_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail=error_str)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.port)

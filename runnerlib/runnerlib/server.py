import logging
import traceback

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, create_model

import classifier
from .settings import settings
import exceptions
from .discovery import get_handler

logger = logging.getLogger('Server')


class ClassificationRequest(BaseModel):
    algorithm: str
    payload: dict


class ClassificationResponse(BaseModel):
    result: dict


app = FastAPI()

# Validar algoritmo válido
# Validar args con handler.get_expected_args()


@app.post("/", response_model=ClassificationResponse, status_code=200)
async def run_algorithm(request: ClassificationRequest):

    handler = get_handler(request.algorithm)

    if not handler.validate_payload(request.payload):
        raise HTTPException(status_code=400, detail=f'Invalid payload. Expected fields: {handler.get_expected_args()}')

    logger.info(f'Found handler {handler}, running on payload {request.payload}')

    try:
        result = handler.call(**request.payload)
        return ClassificationResponse(result=result)

    except exceptions.RequestError as e:
        raise HTTPException(status_code=400, detail=f'Error fetching request image, received {e.response.status_code}')

    except Exception as e:
        error_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail=error_str)


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=settings.port)

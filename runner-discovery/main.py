import logging

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from settings import settings

logger = logging.getLogger('Server')


class AlgorithmRegistrationRequest(BaseModel):
    algorithm: str
    host: str


app = FastAPI()


registry = {}


@app.post('/')
async def register_algorithm(request: AlgorithmRegistrationRequest):
    logger.info(f'Registering algorithm {request.algorithm} as hosted on {request.host}')
    registry[request.algorithm] = request.host


@app.get('/')
async def get_registry():
    return registry


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=settings.port)

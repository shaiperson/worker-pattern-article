import logging
import traceback

import uvicorn
from fastapi import FastAPI, HTTPException

from .settings import settings
from .models import SupportedAlgorithm, request_models_by_algorithm
from .discovery import get_handler
import exceptions

logger = logging.getLogger('Server')

app = FastAPI()


@app.post("/run/{algorithm}")
async def run_algorithm(algorithm: SupportedAlgorithm, payload: dict):
    logger.info(f'Received request to run algorithm {algorithm} on payload {payload}')

    algorithm_name = algorithm.value

    # Validate payload using dynamically generated algorithm-specific model
    request_models_by_algorithm[algorithm_name].validate(payload)

    handler = get_handler(algorithm_name)

    logger.debug(f'Found handler {handler}')

    try:
        result = handler(**payload)
        return dict(result=result)

    except exceptions.RequestError as e:
        raise HTTPException(status_code=400, detail=f'Error fetching request image, received {e.response.status_code}')

    except Exception as e:
        error_str = traceback.format_exc()
        raise HTTPException(status_code=500, detail=error_str)


def run_server():
    logger.debug(f'request_models_by_algorithm: {request_models_by_algorithm}')
    logger.debug(f'Supported algorithms: {list(SupportedAlgorithm)}')
    uvicorn.run(app, host="0.0.0.0", port=settings.port)

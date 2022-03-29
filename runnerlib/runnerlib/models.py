import inspect

from pydantic import create_model, Extra
from enum import Enum

from .discovery import handlers_by_algorithm

request_models_by_algorithm = {}
_supported_algorithm_names = []


class Config:
    extra = Extra.forbid


# Dynamically create
for name, handler in handlers_by_algorithm.items():
    argspec = inspect.getfullargspec(handler)
    typed_argspec = {field: (typehint, ...) for field, typehint in argspec.annotations.items()}
    request_model = create_model(f'AlgorithmRequestModel_{name}', **typed_argspec, __config__=Config)
    request_models_by_algorithm[name] = request_model
    _supported_algorithm_names.append(name)

SupportedAlgorithm = Enum('SupportedAlgorithm', {name: name for name in _supported_algorithm_names})


def get_model_schemas():
    return {name: model.schema() for name, model in request_models_by_algorithm.items()}

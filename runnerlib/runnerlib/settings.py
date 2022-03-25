from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    port: int = Field(env='PORT', default=5000)
    log_level_name: str = Field(env='LOG_LEVEL', default='INFO')
    container_name: str = Field(env='CONTAINER_NAME')
    runner_discovery_container_name: str = Field(env='RUNNER_DISCOVERY_CONTAINER_NAME')
    runner_discovery_port: int = Field(env='RUNNER_DISCOVERY_PORT')

    host: str = None
    runner_discovery_uri: str = None

    def __init__(self):
        super().__init__()
        self.host = f'http://{self.container_name}:{self.port}'
        self.runner_discovery_uri = f'http://{self.runner_discovery_container_name}:{self.runner_discovery_port}'


settings = Settings()

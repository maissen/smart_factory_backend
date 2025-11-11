from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    PROJECT_NAME: str
    PYTHON_VERSION: str = "3.13.2"
    EXTERNAL_PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    MIN_PASSWORD_LENGTH: int = 8
    MIN_PHONE_NUMBER_LENGTH: int = 8

    # User config
    USER_ALLOWED_ROLES: list = ['admin', 'client']

    # Database connection details
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_DRIVER: str = "asyncpg"
    
    @computed_field
    @property
    def POSTGRES_DB_URL(self) -> str:
        return (
            f"postgresql+{self.POSTGRES_DRIVER}://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:5432"
            f"/{self.POSTGRES_DB}"
        )

    
    # Security configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20160 # two weeks


    # InfluxDB configuration
    INFLUXDB_HOST: str
    INFLUXDB_EXTERNAL_PORT: int
    INFLUXDB_TOKEN: str
    INFLUXDB_ORG: str
    INFLUXDB_BUCKET: str

    @computed_field
    @property
    def INFLUXDB_URL(self) -> str:
        return f"{self.INFLUXDB_HOST}:{self.INFLUXDB_EXTERNAL_PORT}"


    # machines config
    MACHINE_POSSIBLE_STATUS: list = ["Running", "Idle", "Maintenance", "Stopped"]
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

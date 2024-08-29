from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)
from pydantic_core import MultiHostUrl
from pydantic import (
    computed_field,
    PostgresDsn,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    ) # Pydantic .env support
    SECRET_KEY:str
    
    # settings for db 
    DB_NAME:str
    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:int = 5432
    
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self)->PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )
    
    # settings for tokens
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 15 
    REFRESH_TOKEN_EXPIRE_MINUTES:int = 60*24 # 1 day (change later)
    
settings = Settings()
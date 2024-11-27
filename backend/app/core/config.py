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
    PRIVATE_KEY:str
    PUBLIC_KEY:str
    
    @property
    def private_key(self) -> str:
        """Convert escaped \\n to actual newlines in the private key."""
        return self.PRIVATE_KEY.replace("\\n", "\n")
    
    @property
    def public_key(self) -> str:
        """Convert escaped \\n to actual newlines in the public key."""
        return self.PUBLIC_KEY.replace("\\n", "\n")
    
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
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 15 # change later
    REFRESH_TOKEN_EXPIRE_MINUTES:int = 60*24 # 1 day (change later)
    
    # settings for initial superuser
    FIRST_SUPERUSER:str
    FIRST_SUPERUSER_PASSWORD:str
    
    ALGORITHM:str = 'RS256'
    
settings = Settings()
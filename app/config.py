# app/config.py
# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    EMAIL: str = Field("aluyapeter7@gmail.com", description="Your email address")
    NAME: str = Field("Peter Aluya", description="Your full name")
    STACK: str = Field("Python/FastAPI", description="Your backend stack")
    CATFACT_URL: str = Field("https://catfact.ninja/fact", description="Cat fact API URL")
    EXTERNAL_TIMEOUT: float = Field(5.0, description="External API timeout in seconds")

    # Since we're hardcoding, env_file config is not needed, but keeping the config structure
    model_config = SettingsConfigDict()


settings = Settings()  # type: ignore

# from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import Field


# class Settings(BaseSettings):
#     EMAIL: str = Field(..., description="Your email address")
#     NAME: str = Field(..., description="Your full name")
#     STACK: str = Field("Python/FastAPI", description="Your backend stack")
#     CATFACT_URL: str = Field("https://catfact.ninja/fact", description="Cat fact API URL")
#     EXTERNAL_TIMEOUT: float = Field(5.0, description="External API timeout in seconds")

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8"
#     )


# settings = Settings() # type: ignore

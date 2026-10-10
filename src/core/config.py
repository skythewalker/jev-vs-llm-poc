from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    openai_api_key: str
    jev_api_key: str
    gpt_model: str = "gpt-5.4-mini"
    jev_model: str = "jev-latest"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
        
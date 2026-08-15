from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Women's Health Tracker"
    app_version: str = "1.0.0"
    debug: bool = True
    hf_token: str = ""
    database_url: str

    supabase_url: str
    supabase_key: str

    class Config:
        env_file = ".env"


settings = Settings()
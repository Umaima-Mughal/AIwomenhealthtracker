from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Women's Health Tracker"
    app_version: str = "1.0.0"
    debug: bool = True
    hf_token: str = ""
    database_url: str

    supabase_url: str
    supabase_key: str

    # CORS settings for the React/Vite frontend
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"  ##

    class Config:
        env_file = ".env"

    @property
    def cors_origins_list(self) -> list[str]:   ##
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
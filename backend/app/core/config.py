from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SLD Digital Twin Platform"
    environment: str = "dev"
    database_url: str = "sqlite:///./sld.db"
    storage_path: str = "./storage"
    reports_path: str = "./reports"
    symbol_model_path: str = "./models/symbol_classifier.joblib"
    allow_origins: list[str] = ["*"]


settings = Settings()

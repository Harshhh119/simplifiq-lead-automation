from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    GOOGLE_SHEET_ID: str = ""
    GOOGLE_DRIVE_FOLDER_ID: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

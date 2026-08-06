from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str

    JWT_SECRET: str

    JWT_ALGORITHM: str = "HS256"

    OLLAMA_MODEL: str = "llama3.2:3b"

    CHROMA_PATH: str = "./chroma_db"

    class Config:

        env_file = ".env"



settings = Settings()
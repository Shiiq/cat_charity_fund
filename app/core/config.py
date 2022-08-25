from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Сервис пожертвований QRKot'
    database_url: str
    description: str
    secret: str = 'extra gin please'

    class Config:
        env_file = '../.env'


settings = Settings()

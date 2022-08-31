from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
# from core.init_db import create_first_superuser


app = FastAPI(
    title=settings.app_title,
    description=settings.description
)
app.include_router(main_router)


# @app.on_event('startup')
# async def startup():
#     print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))
#     await create_first_superuser()

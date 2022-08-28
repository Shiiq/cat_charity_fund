from fastapi import APIRouter

from .endpoints import charity_project_router, user_router

main_router = APIRouter()
main_router.include_router(charity_project_router, prefix='/charity-project')
main_router.include_router(user_router)

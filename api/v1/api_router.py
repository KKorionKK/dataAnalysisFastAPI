from fastapi import APIRouter
from api.v1.routes.files import files_router
from api.v1.routes.data import data_router

main_router = APIRouter()

main_router.include_router(files_router)
main_router.include_router(data_router)

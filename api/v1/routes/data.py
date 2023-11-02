from fastapi import APIRouter, Depends
from api.services.schemas import RequestForDiagram
from api.services.database import get_session
from api.v1.services.dataProcessing import get_diagram_data

data_router = APIRouter(prefix="/data", tags=["Get data for diagram"])


@data_router.post("/")
async def get_data_for_diagram(data: RequestForDiagram, session=Depends(get_session)):
    """
    Получаем на вход значения, по которым хотим получить данные
    """
    return await get_diagram_data(request=data, session=session)

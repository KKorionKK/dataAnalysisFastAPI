from api.services.schemas import RequestForDiagram
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from api.services.models import Value, Project
from fastapi import HTTPException, status


async def get_diagram_data(request: RequestForDiagram, session: AsyncSession):
    return await get_data_from_db(request, session)


async def get_data_from_db(request: RequestForDiagram, session: AsyncSession):
    data = (
        await session.scalars(
            select(Value)
            .join(Project, Project.id == Value.project_id)
            .where(
                and_(
                    Project.file_id == request.file_id,
                    func.DATE_PART("year", Value.date) == request.year,
                )
            )
        )
    ).all()
    data_list = [item.to_dict(request.value_type) for item in data]
    if data_list == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data for this input values",
        )
    return data_list

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from api.services.models import File, Value, Project
from datetime import datetime
from api.services.schemas import FileIDResponse
from fastapi import HTTPException, status


async def handle_file(file: bytes, filename: str, session: AsyncSession):
    fileInDb = File(filename, file)
    file_dataframe = pd.read_excel(file, sheet_name="data", header=None)
    if file_dataframe.empty:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="File must be not empty"
        )
    dates, project_values, projects = await get_data_from_dataframe(file_dataframe)
    valuesInDb, projectsInDB = await prepare_data(
        dates, project_values, projects, fileInDb
    )

    return await attempt_instances_to_db(fileInDb, valuesInDb, projectsInDB, session)


async def get_data_from_dataframe(dataframe: pd.DataFrame):
    pd.DataFrame(columns=["Код проекта", "Наименование проекта"])
    pd.DataFrame(columns=["План", "Факт", "Дата"])

    projects: list[list] = dataframe[2::].iloc[:, [0, 1]].values.tolist()
    dates_: list = dataframe.iloc[:1, 2::].values.tolist()[0]
    dates = []
    for date in dates_:
        if isinstance(date, datetime):
            dates.append(date)
    values = dataframe.iloc[2:, 2::]
    values.fillna(0, inplace=True)
    project_values = list()
    for index, row in values.iterrows():
        row_list: list = row.values.tolist()
        project_values.append(row_list)
    return dates, project_values, projects


async def prepare_data(
    dates: list, values: list[list], projects: list[list], file: File
):
    valuesInDb = list()
    projectsInDb = list()

    for projectList in projects:
        projectsInDb.append(Project(projectList[0], projectList[1], file))

    c = 0
    for valuesList in values:
        for i in range(len(dates)):
            valuesInDb.append(
                Value(valuesList.pop(0), valuesList.pop(0), dates[i], projectsInDb[c])
            )
        c += 1

    return valuesInDb, projectsInDb


async def attempt_instances_to_db(
    file: File, values: list[Value], projects: list[Project], session: AsyncSession
):
    session.add(file)
    session.add_all(projects)
    session.add_all(values)
    await session.flush()
    file_id = file.id
    await session.commit()
    return FileIDResponse(file_id=file_id)


async def get_file_by_id(file_id: int, session: AsyncSession):
    file = await session.get(File, file_id)
    if file is not None:
        return file
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="There is no file with this id"
    )

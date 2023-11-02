from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
import io
from api.services.database import get_session
from api.v1.services.fileProcessing import handle_file, get_file_by_id

files_router = APIRouter(prefix="/files", tags=["File Upload or Download"])


@files_router.post("/upload")
async def get_file_for_upload(file: UploadFile, session=Depends(get_session)):
    """
    Получаем на вход файл формата xlsx, если формат неверный, то получаем ошибку

    После загрузки файла выводим id файла
    """
    if (
        file.content_type
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ):
        return await handle_file(
            file=await file.read(), filename=file.filename, session=session
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid file format"
        )


@files_router.get("/download/{file_id}")
async def download_file(file_id: int, session=Depends(get_session)):
    """
    Скачиваем файл с тем же id
    """
    file = await get_file_by_id(file_id=file_id, session=session)
    if isinstance(file, HTTPException):
        raise file
    return StreamingResponse(
        content=io.BytesIO(file.file),
        headers={"Content-Disposition": f"attachment; filename={file.filename}"},
    )

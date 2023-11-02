import pytest
from httpx import AsyncClient
from app import app
import json

class TestAPI:
    @pytest.mark.asyncio
    async def test_null_response(self):
        test_file = "./tests/null.xlsx"
        files = {'file': ('null.xlsx', open(test_file, 'rb'))}
        async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
            upload_null_file = await ac.post(
                "files/upload",
                files=files,
            )
        assert upload_null_file.status_code == 406
    
    @pytest.mark.asyncio
    async def test_invalid_fileformat_response(self):
        test_file = "./tests/invalid_format.txt"
        files = {'file': ('invalid_format.txt', open(test_file, 'rb'))}
        async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
            upload_invalid_file = await ac.post(
                "files/upload",
                files=files,
            )
        assert upload_invalid_file.status_code == 406
    
    @pytest.mark.asyncio
    async def test_valid_file(self):
        test_file = "./tests/example.xlsx"
        files = {'file': ('example.xlsx', open(test_file, 'rb'))}
        async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
            upload_valid_file = await ac.post(
                "files/upload",
                files=files,
            )
        assert upload_valid_file.status_code == 200

    @pytest.mark.asyncio
    async def test_download_file(self):
        async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
            upload_valid_file = await ac.get(
                "files/download/1"
            )
        assert upload_valid_file.status_code == 200


    @pytest.mark.asyncio
    async def test_get_data(self):
        payload = {
            "file_id": 1,
            "year": 2022,
            "value_type": "fact"
        }
        async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
            upload_valid_file = await ac.post(
                "data/",
                content=json.dumps(payload)
            )
        assert upload_valid_file.status_code == 200
    
    @pytest.mark.asyncio
    async def test_get_data_wrong_request(self):
        payload = {
            "file_id": 1,
            "year": 2022,
            "value_type": "string"
        }
        async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
            upload_valid_file = await ac.post(
                "data/",
                content=json.dumps(payload)
            )
        assert upload_valid_file.status_code == 422
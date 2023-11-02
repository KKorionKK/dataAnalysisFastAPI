from fastapi import FastAPI
from api.v1.api_router import main_router
from contextlib import asynccontextmanager
import uvicorn
from api.services.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

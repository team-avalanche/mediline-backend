from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from api.config import CONFIG

from api.models.user import UserInDB

description = """

Schedule appointments with Doctors. Reduce wait time.

"""
app = FastAPI(title="Doctor Booking API", version="0.0.1", description=description)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index() -> dict:
    return {"message": "server is up"}


@app.on_event("startup")
async def start_app():
    client = AsyncIOMotorClient(CONFIG.mongo_uri)
    db = client[CONFIG.db_name]
    await init_beanie(database=db, document_models=[UserInDB])


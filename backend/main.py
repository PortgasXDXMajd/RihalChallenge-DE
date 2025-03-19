from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
import app.routers.crime_router as crime_router
from fastapi.middleware.cors import CORSMiddleware
from app.helpers.database_helper import DatabaseHelper

@asynccontextmanager
async def lifespan(app: FastAPI):
    DatabaseHelper.seed()
    yield

app = FastAPI(title="Rihal Data Engineering Challenge", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crime_router.router, tags=["Auth Controller"])

@app.get("/")
def GetHomePage():
    return HTMLResponse("<h1>Data Engineering Challenge Rihal - Backend</h1>")
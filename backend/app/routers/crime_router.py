from fastapi import APIRouter, Body
from sqlalchemy import text
from app.helpers.response_helper import ResponseHelper
from app.helpers.database_helper import DatabaseHelper

router = APIRouter(prefix="/crime")


@router.get("/")
async def get_crime_data():
    try:
        db_engine = DatabaseHelper.get_db_engine()
        with db_engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM crime_data;"))
            count = result.scalar_one()
        return ResponseHelper.success(count)
    except Exception as e:
        return ResponseHelper.error(msg=str(e))
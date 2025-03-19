from fastapi import APIRouter, Body
from sqlalchemy import text
from app.helpers.response_helper import ResponseHelper
from app.helpers.database_helper import DatabaseHelper
from app.helpers.sql_query_helper import SqlHelper

router = APIRouter(prefix="/crime")


@router.get("/required-stats")
async def get_crime_data():
    try:
        db_engine = DatabaseHelper.get_db_engine()
        with db_engine.connect() as connection:
            sql_result = connection.execute(text(SqlHelper.get_required_stat_query()))
            result = [dict(row) for row in sql_result.mappings()]
        return ResponseHelper.success(result)
    except Exception as e:
        return ResponseHelper.error(msg=str(e))
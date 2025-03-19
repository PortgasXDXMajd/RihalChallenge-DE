import os
from pandas import DataFrame
from sqlalchemy import create_engine
from app.pipelines.pipelines_processor import PipelineProcessor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://rihal_user:rihal_pwd@db:5432/rihal_db")

class DatabaseHelper:
    table_name = "crime_data"

    data_df = None

    @classmethod
    def get_db_engine(cls):
        return create_engine(DATABASE_URL)
    
    @classmethod
    def seed(cls):
        cls._run_piplelines()
        cls._store_df_to_db()

    @classmethod
    def _run_piplelines(cls) -> DataFrame:
        try:
            processor = PipelineProcessor()
            cls.data_df = processor.process()
        except Exception as e:
            print(f"Failed to run pipelines: {e}")
            raise e
        
    @classmethod
    def _store_df_to_db(cls):
        try:
            engine = cls.get_db_engine()
            cls.data_df.to_sql(cls.table_name, engine, if_exists="replace", index=False)
        except Exception as e:
            print(f"Failed to store DataFrame in DB: {e}")
            raise e
        
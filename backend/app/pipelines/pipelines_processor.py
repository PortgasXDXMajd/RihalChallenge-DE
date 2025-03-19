from app.pipelines.crime_data_pipeline import CrimeDataPipeline
from app.pipelines.district_info_pipeline import DistrictInfoPipeline


class PipelineProcessor:
    def __init__(self):
        self.crime_data_pipeline = CrimeDataPipeline()
        self.district_info_pipeline = DistrictInfoPipeline()
    
    def process(self):
        crime_data_df = self.crime_data_pipeline.process()
        district_info_df = self.district_info_pipeline.process()
        
        combined_df = crime_data_df.merge(district_info_df, 
            on='district_id',
            how='inner',
            suffixes=('_pipe1', '_pipe2')
        )
        
        return combined_df
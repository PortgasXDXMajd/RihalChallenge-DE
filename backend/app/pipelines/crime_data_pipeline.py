import json
import os
import pandas as pd

class CrimeDataPipeline:
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), "data/crime_data.json")

        self.spelling_correction = {
            "thaft": "theft",
            "frued": "fraud",
            "assult": "assault"
        }

    def load_data(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return pd.DataFrame(data)

    def remove_invalid_records(self, df:pd.DataFrame):
        return df[df['crime_type'].notna() & (df['crime_type'] != '')]

    def correct_spelling(self, text):
        return self.spelling_correction[text.lower()] if text.lower() in self.spelling_correction else text.lower()

    def convert_to_km(self, distance_str:str):
        value = float(distance_str.split()[0])
        unit = distance_str.split()[1].lower()
        val_in_km = value * 1.60934 if unit in ['mile', 'miles'] else value
        return round(val_in_km, 2)

    def split_timestamp(self, df):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['day_of_week'] = df['timestamp'].dt.day_name()
        df['date'] = df['timestamp'].dt.date
        df['time'] = df['timestamp'].dt.time
        df.drop(columns=['timestamp'], inplace=True)
        return df

    def process(self):
        df = self.load_data()

        df = self.remove_invalid_records(df)
        
        # no need for apply (bad preformance) but the dataset is small so it is fine
        df['crime_type'] = df['crime_type'].apply(self.correct_spelling)
        
        df['nearest_police_patrol'] = df['nearest_police_patrol'].apply(self.convert_to_km)
                
        df = self.split_timestamp(df)
        
        return df
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class SatelliteDataLoader:
    def __init__(self, data_dir: str = "data/raw/satellite"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def load_historical_data(self, start_date: datetime, end_date: datetime, 
                           area_of_interest: dict) -> pd.DataFrame:
        """Load or generate historical ocean data"""
        current_date = start_date
        all_data = []
        
        while current_date <= end_date:
            # Generate synthetic data for each day
            all_data.append({
                'date': current_date,
                'sst': 28 + 2 * np.random.random(),  # Random SST around 28°C
                'chlorophyll': 0.5 + 0.5 * np.random.random(),  # Random chlorophyll
                'location': 'indonesia_waters'
            })
            
            current_date += timedelta(days=1)
        
        return pd.DataFrame(all_data)
    
    def fetch_sample_data(self):
        """Simple sample data for testing"""
        return pd.DataFrame({
            'date': [datetime(2024, 1, 1), datetime(2024, 1, 2)],
            'sst': [28.5, 29.1],
            'chlorophyll': [0.8, 0.9]
        })

if __name__ == "__main__":
    loader = SatelliteDataLoader()
    print("Sample Data:")
    print(loader.fetch_sample_data())
    
    # Test historical data
    aoi = {'lat_min': -11.0, 'lat_max': 6.0, 'lon_min': 95.0, 'lon_max': 141.0}
    historical_data = loader.load_historical_data(
        datetime(2024, 1, 1), 
        datetime(2024, 1, 5), 
        aoi
    )
    print("\nHistorical Data:")
    print(historical_data)

#!/bin/bash

echo "🚀 Creating simple data processing modules..."

# Buat directory jika belum ada
mkdir -p src/data_processing

# Buat satellite_loader.py dengan echo
echo "import pandas as pd
from datetime import datetime

class SatelliteDataLoader:
    def fetch_sample_data(self):
        return pd.DataFrame({
            'date': [datetime(2024, 1, 1), datetime(2024, 1, 2)],
            'sst': [28.5, 29.1],
            'chlorophyll': [0.8, 0.9]
        })

if __name__ == \"__main__\":
    loader = SatelliteDataLoader()
    print(loader.fetch_sample_data())" > src/data_processing/satellite_loader.py

# Buat data_cleaner.py
echo "import pandas as pd

class DataCleaner:
    def clean_data(self, df):
        return df.dropna()

if __name__ == \"__main__\":
    cleaner = DataCleaner()
    print(\"DataCleaner ready!\")" > src/data_processing/data_cleaner.py

# Update main.py
echo "from regulatory_engine.compliance_checker import FisheriesCompliance
from data_processing.satellite_loader import SatelliteDataLoader
from datetime import datetime

def main():
    print(\"🚀 Fisheries AI System - Basic Data Processing\")
    
    # Test compliance
    compliance = FisheriesCompliance()
    result = compliance.check_fishing_approval(
        species=\"tuna\", location=[95.5, -5.5],
        date=datetime(2024, 1, 15), gear_type=\"hand_line\", proposed_catch=3000
    )
    print(f\"Compliance: {'✅' if result['approved'] else '❌'}\")
    
    # Test data loading
    loader = SatelliteDataLoader()
    data = loader.fetch_sample_data()
    print(f\"Sample data: {len(data)} rows\")
    
    print(\"✅ System working!\")

if __name__ == \"__main__\":
    main()" > src/main.py

echo "✅ Setup complete! Run: python src/main.py"

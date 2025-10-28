import sys
import os

# Fix Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from regulatory_engine.compliance_checker import FisheriesCompliance
from data_processing.satellite_loader import SatelliteDataLoader
from data_processing.data_cleaner import DataCleaner
from ai_models.fish_predictor import FishLocationPredictor
from datetime import datetime

def main():
    print("🚀 Fisheries AI System - Now with AI Prediction!")
    print("=" * 50)
    
    # 1. Test Regulatory Compliance
    compliance = FisheriesCompliance()
    result = compliance.check_fishing_approval(
        species="tuna", location=[95.5, -5.5],
        date=datetime(2024, 1, 15), gear_type="hand_line", proposed_catch=3000
    )
    print(f"📋 Compliance Check: {'✅ APPROVED' if result['approved'] else '❌ REJECTED'}")
    if result['violations']:
        print(f"   Violations: {result['violations']}")
    
    print("=" * 50)
    
    # 2. Test Data Processing
    loader = SatelliteDataLoader()
    cleaner = DataCleaner()
    
    aoi = {'lat_min': -11.0, 'lat_max': 6.0, 'lon_min': 95.0, 'lon_max': 141.0}
    raw_data = loader.load_historical_data(
        datetime(2024, 1, 1), 
        datetime(2024, 1, 5), 
        aoi
    )
    
    cleaned_data = cleaner.clean_ocean_data(raw_data)
    print(f"🌊 Ocean Data: {len(cleaned_data)} days collected")
    
    print("=" * 50)
    
    # 3. Test AI Prediction
    predictor = FishLocationPredictor()
    training_data = predictor.prepare_training_data(cleaned_data)
    
    print(f"🤖 Training AI Model with {len(training_data)} samples...")
    predictor.train_model(training_data, 'tuna')
    
    # Get predictions
    predictions = predictor.predict_fish_locations(cleaned_data, 'tuna')
    
    print("🔮 AI Fishing Recommendations:")
    for _, row in predictions.iterrows():
        prob = row['tuna_probability']
        rec = row['recommendation']
        print(f"   📅 {row['date'].strftime('%Y-%m-%d')}: {prob:.1%} probability → {rec}")
    
    print("=" * 50)
    print("✅ AI-Powered Fisheries System Fully Operational!")

if __name__ == "__main__":
    main()

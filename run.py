#!/usr/bin/env python3
import sys
import os

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'src'))

try:
    from regulatory_engine.compliance_checker import FisheriesCompliance
    from data_processing.satellite_loader import SatelliteDataLoader
    from datetime import datetime
    
    print("🚀 Fisheries AI System - Basic Data Processing")
    
    # Test compliance
    compliance = FisheriesCompliance()
    result = compliance.check_fishing_approval(
        species="tuna", location=[95.5, -5.5],
        date=datetime(2024, 1, 15), gear_type="hand_line", proposed_catch=3000
    )
    print(f"Compliance: {'✅' if result['approved'] else '❌'}")
    
    # Test data loading
    loader = SatelliteDataLoader()
    data = loader.fetch_sample_data()
    print(f"Sample data: {len(data)} rows")
    print("✅ System working!")
    
except Exception as e:
    print(f"Error: {e}")
    print("Troubleshooting...")
    
    # Debug info
    print(f"Current directory: {current_dir}")
    print(f"Python path: {sys.path}")
    
    # Check if files exist
    import os
    print(f"regulatory_engine exists: {os.path.exists('src/regulatory_engine')}")
    print(f"compliance_checker.py exists: {os.path.exists('src/regulatory_engine/compliance_checker.py')}")

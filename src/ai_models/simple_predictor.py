import pandas as pd
import numpy as np
import os

class SimpleFishPredictor:
    def __init__(self):
        pass
    
    def predict(self, ocean_data: pd.DataFrame, species: str = 'tuna') -> pd.DataFrame:
        """Simple heuristic-based fish prediction"""
        results = ocean_data.copy()
        
        if 'date' in results.columns:
            results['month'] = results['date'].dt.month
        
        # Simple rules-based prediction
        if species == 'tuna':
            # Tuna like warm waters (26-30°C) with moderate chlorophyll
            results['probability'] = np.clip(
                (results['sst'] - 25) * 0.1 + (results['chlorophyll'] - 0.5) * 0.2, 
                0, 1
            )
        elif species == 'skipjack':
            # Skipjack prefer slightly cooler waters
            results['probability'] = np.clip(
                (results['sst'] - 24) * 0.08 + (results['chlorophyll'] - 0.6) * 0.15,
                0, 1
            )
        else:
            results['probability'] = 0.5
        
        # Add recommendation
        results['recommendation'] = results['probability'].apply(
            lambda x: 'HIGH' if x > 0.7 else 'MEDIUM' if x > 0.4 else 'LOW'
        )
        
        return results

if __name__ == "__main__":
    # Test dengan sample data
    sample_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=3),
        'sst': [28.5, 29.1, 27.8],
        'chlorophyll': [0.8, 0.9, 0.6]
    })
    
    predictor = SimpleFishPredictor()
    predictions = predictor.predict(sample_data, 'tuna')
    
    print("🤖 Simple Fish Predictor Results:")
    print(predictions[['date', 'sst', 'probability', 'recommendation']])

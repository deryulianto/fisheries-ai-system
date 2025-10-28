import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os
import sys

# Add parent directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..')
sys.path.insert(0, src_dir)

from data_processing.satellite_loader import SatelliteDataLoader
from data_processing.data_cleaner import DataCleaner

class FishLocationPredictor:
    def __init__(self, model_dir: str = "models/trained_models"):
        self.model_dir = model_dir
        self.model = None
        os.makedirs(model_dir, exist_ok=True)
    
    def prepare_training_data(self, ocean_data: pd.DataFrame, 
                            historical_catch: pd.DataFrame = None) -> pd.DataFrame:
        """Prepare training data with features for fish prediction"""
        
        # For demo, we'll create synthetic training data
        np.random.seed(42)
        
        training_data = []
        for _, row in ocean_data.iterrows():
            sst = row['sst']
            chlorophyll = row['chlorophyll']
            
            # Fish probability based on ocean conditions
            tuna_probability = np.clip(
                (sst - 25) * 0.1 + (chlorophyll - 0.5) * 0.2 + np.random.normal(0, 0.1),
                0, 1
            )
            
            skipjack_probability = np.clip(
                (sst - 24) * 0.08 + (chlorophyll - 0.6) * 0.15 + np.random.normal(0, 0.1),
                0, 1
            )
            
            training_data.append({
                'date': row['date'],
                'sst': sst,
                'chlorophyll': chlorophyll,
                'tuna_probability': tuna_probability,
                'skipjack_probability': skipjack_probability,
                'month': row['date'].month,
                'season': (row['date'].month % 12 + 3) // 3
            })
        
        return pd.DataFrame(training_data)
    
    def train_model(self, training_data: pd.DataFrame, target_species: str = 'tuna'):
        """Train machine learning model to predict fish locations"""
        
        features = ['sst', 'chlorophyll', 'month', 'season']
        X = training_data[features]
        y = training_data[f'{target_species}_probability']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        
        print(f"✅ Model trained for {target_species}")
        print(f"📊 Mean Absolute Error: {mae:.3f}")
        
        model_path = os.path.join(self.model_dir, f'{target_species}_predictor.joblib')
        joblib.dump(self.model, model_path)
        print(f"💾 Model saved to: {model_path}")
        
        return mae
    
    def predict_fish_locations(self, ocean_conditions: pd.DataFrame, 
                             species: str = 'tuna') -> pd.DataFrame:
        """Predict fish probability for given ocean conditions"""
        
        if self.model is None:
            model_path = os.path.join(self.model_dir, f'{species}_predictor.joblib')
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
            else:
                print("⚠️ No trained model found. Using heuristic prediction.")
                return self._heuristic_prediction(ocean_conditions, species)
        
        features = ['sst', 'chlorophyll', 'month', 'season']
        
        if 'month' not in ocean_conditions.columns and 'date' in ocean_conditions.columns:
            ocean_conditions['month'] = ocean_conditions['date'].dt.month
            ocean_conditions['season'] = (ocean_conditions['month'] % 12 + 3) // 3
        
        X_pred = ocean_conditions[features]
        predictions = self.model.predict(X_pred)
        
        results = ocean_conditions.copy()
        results[f'{species}_probability'] = predictions
        results['recommendation'] = results[f'{species}_probability'].apply(
            lambda x: 'HIGH' if x > 0.7 else 'MEDIUM' if x > 0.4 else 'LOW'  # Fixed typo: LOVY → LOW
        )
        
        return results
    
    def _heuristic_prediction(self, ocean_conditions: pd.DataFrame, species: str) -> pd.DataFrame:
        """Fallback heuristic prediction when no model is trained"""
        results = ocean_conditions.copy()
        
        if species == 'tuna':
            results['tuna_probability'] = np.clip(
                (results['sst'] - 25) * 0.1 + (results['chlorophyll'] - 0.5) * 0.2, 0, 1
            )
        else:
            results[f'{species}_probability'] = 0.5
            
        results['recommendation'] = 'HEURISTIC'
        return results

# Example usage dengan error handling
if __name__ == "__main__":
    try:
        print("🤖 Testing Fish Location Predictor...")
        
        # Generate sample data
        loader = SatelliteDataLoader()
        cleaner = DataCleaner()
        
        aoi = {'lat_min': -11.0, 'lat_max': 6.0, 'lon_min': 95.0, 'lon_max': 141.0}
        
        # Create simple test data untuk avoid dependencies
        test_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=5),
            'sst': [28.5, 29.1, 28.8, 29.5, 28.2],
            'chlorophyll': [0.8, 0.9, 0.7, 0.85, 0.75]
        })
        
        cleaned_data = cleaner.clean_ocean_data(test_data)
        
        # Initialize and train predictor
        predictor = FishLocationPredictor()
        training_data = predictor.prepare_training_data(cleaned_data)
        
        print(f"📊 Training data shape: {training_data.shape}")
        
        # Train model
        predictor.train_model(training_data, 'tuna')
        
        # Make predictions
        predictions = predictor.predict_fish_locations(cleaned_data, 'tuna')
        print(f"🔮 Prediction sample:")
        print(predictions[['date', 'sst', 'tuna_probability', 'recommendation']].head())
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Troubleshooting import issues...")

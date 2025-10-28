import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

class DataCleaner:
    def __init__(self):
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='mean')
    
    def clean_ocean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess oceanographic data"""
        df_clean = df.copy()
        
        # Handle missing values
        numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            df_clean[numeric_columns] = self.imputer.fit_transform(df_clean[numeric_columns])
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        # Add temporal features
        if 'date' in df_clean.columns:
            df_clean['date'] = pd.to_datetime(df_clean['date'])
            df_clean['day_of_year'] = df_clean['date'].dt.dayofyear
            df_clean['month'] = df_clean['date'].dt.month
            df_clean['season'] = (df_clean['month'] % 12 + 3) // 3
        
        return df_clean
    
    def create_fishing_features(self, ocean_data: pd.DataFrame, 
                              historical_catch: pd.DataFrame = None) -> pd.DataFrame:
        """Create features for fish prediction model"""
        features = ocean_data.copy()
        
        # Basic feature engineering
        if 'sst' in features.columns and 'chlorophyll' in features.columns:
            features['sst_chlorophyll_interaction'] = features['sst'] * features['chlorophyll']
        
        return features
    
    def scale_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Scale features for machine learning"""
        numeric_columns = features.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            features_scaled = features.copy()
            features_scaled[numeric_columns] = self.scaler.fit_transform(features[numeric_columns])
            return features_scaled
        return features

# Example usage
if __name__ == "__main__":
    # Test the data cleaner
    sample_data = pd.DataFrame({
        'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'sst': [28.5, 29.1, 27.8],
        'chlorophyll': [0.8, 0.9, 0.6]
    })
    
    cleaner = DataCleaner()
    cleaned_data = cleaner.clean_ocean_data(sample_data)
    
    print("Original Data:")
    print(sample_data)
    print("\nCleaned Data:")
    print(cleaned_data)
    
    features = cleaner.create_fishing_features(cleaned_data)
    print("\nFeatures:")
    print(features)

from flask import Flask, render_template, jsonify, request
import sys
import os
import pandas as pd
from datetime import datetime

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..')
sys.path.insert(0, src_dir)

from regulatory_engine.compliance_checker import FisheriesCompliance
from data_processing.satellite_loader import SatelliteDataLoader
from data_processing.data_cleaner import DataCleaner
from ai_models.fish_predictor import FishLocationPredictor

app = Flask(__name__)

# Initialize components
compliance_engine = FisheriesCompliance()
data_loader = SatelliteDataLoader()
data_cleaner = DataCleaner()
predictor = FishLocationPredictor()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/compliance-check', methods=['POST'])
def compliance_check():
    """API for compliance checking"""
    try:
        data = request.json
        result = compliance_engine.check_fishing_approval(
            species=data['species'],
            location=[data.get('lon', 106.0), data.get('lat', -6.0)],  # Default: Jakarta area
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            gear_type=data['gear_type'],
            proposed_catch=float(data['proposed_catch'])
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/fish-prediction', methods=['POST'])
def fish_prediction():
    """API for fish location prediction"""
    try:
        data = request.json
        
        # Generate ocean data for prediction
        aoi = {
            'lat_min': data.get('lat_min', -8.0),   # More realistic Indonesia bounds
            'lat_max': data.get('lat_max', 5.0),
            'lon_min': data.get('lon_min', 95.0),
            'lon_max': data.get('lon_max', 141.0)
        }
        
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        
        # Get ocean data
        raw_data = data_loader.load_historical_data(start_date, end_date, aoi)
        cleaned_data = data_cleaner.clean_ocean_data(raw_data)
        
        # Get predictions
        predictions = predictor.predict_fish_locations(cleaned_data, data['species'])
        
        # Convert to JSON-serializable format
        results = []
        for _, row in predictions.iterrows():
            results.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'sst': float(row['sst']),
                'chlorophyll': float(row['chlorophyll']),
                'probability': float(row[f"{data['species']}_probability"]),
                'recommendation': row['recommendation']
            })
        
        return jsonify({
            'predictions': results,
            'summary': {
                'total_days': len(results),
                'high_recommendations': len([r for r in results if r['recommendation'] == 'HIGH']),
                'avg_probability': sum(r['probability'] for r in results) / len(results)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/dashboard-stats')
def dashboard_stats():
    """API for dashboard statistics"""
    # Generate sample stats
    stats = {
        'total_predictions': 247,
        'compliance_checks': 156,
        'avg_sustainability_score': 0.76,
        'high_probability_days': 42,
        'protected_areas_monitored': 18
    }
    return jsonify(stats)

if __name__ == '__main__':
    print("🚀 Starting Fisheries AI Dashboard...")
    print("🌐 Access at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

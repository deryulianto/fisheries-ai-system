import yaml
from datetime import datetime

class FisheriesCompliance:
    def __init__(self, config_path: str = "config/regulatory_rules.yaml"):
        self.regulations = self.load_regulations(config_path)
    
    def load_regulations(self, config_path: str):
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading regulations: {e}")
            return {}
    
    def check_fishing_approval(self, species: str, location: list, 
                             date: datetime, gear_type: str, proposed_catch: float):
        violations = []
        
        # Simple check for demo
        if species == "tuna" and date.month in [1, 2]:  # Jan-Feb closed
            violations.append(f"Closed season for {species}")
        
        if gear_type == "dynamite":
            violations.append("Prohibited gear type")
            
        return {
            "approved": len(violations) == 0,
            "violations": violations,
            "sustainability_score": 0.8
        }

if __name__ == "__main__":
    compliance = FisheriesCompliance()
    result = compliance.check_fishing_approval(
        species="tuna",
        location=[95.5, -5.5],
        date=datetime(2024, 1, 15),
        gear_type="hand_line",
        proposed_catch=3000
    )
    print(f"Result: {result}")

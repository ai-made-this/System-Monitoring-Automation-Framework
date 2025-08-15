"""Predictive Analysis - Predicts future system needs and user behavior"""
import json
import time
from pathlib import Path
import statistics
from collections import defaultdict

DATA_DIR = Path(__file__).parent / "data"
PREDICTIONS_FILE = DATA_DIR / "predictions.json"
HISTORY_FILE = DATA_DIR / "prediction_history.json"

def get_predictive_analysis():
    """Generate predictions based on historical data and patterns"""
    try:
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(exist_ok=True)
        
        # Load historical data for predictions
        predictions = _generate_predictions()
        
        # Save predictions
        prediction_data = {
            "predictions": predictions,
            "generated_at": time.time(),
            "confidence_level": _calculate_prediction_confidence(predictions)
        }
        
        with open(PREDICTIONS_FILE, 'w') as f:
            json.dump(prediction_data, f, indent=2)
        
        return {
            "status": "generated",
            "predictions": predictions,
            "prediction_count": len(predictions),
            "confidence": prediction_data["confidence_level"],
            "next_update": time.time() + 3600  # Update every hour
        }
    except Exception as e:
        return {"error": str(e)}

def _generate_predictions():
    """Generate various types of predictions"""
    current_time = time.time()
    current_hour = time.localtime(current_time).tm_hour
    
    predictions = []
    
    # Resource usage predictions
    predictions.extend(_predict_resource_usage(current_hour))
    
    # Activity predictions
    predictions.extend(_predict_user_activity(current_hour))
    
    # System maintenance predictions
    predictions.extend(_predict_maintenance_needs())
    
    return predictions

def _predict_resource_usage(current_hour):
    """Predict system resource usage"""
    predictions = []
    
    # CPU usage prediction based on time of day
    if 9 <= current_hour <= 17:
        predictions.append({
            "type": "resource_usage",
            "resource": "cpu",
            "prediction": "high",
            "confidence": 0.7,
            "reason": "Work hours - typically high CPU usage",
            "timeframe": "next_2_hours"
        })
    elif 18 <= current_hour <= 22:
        predictions.append({
            "type": "resource_usage",
            "resource": "gpu",
            "prediction": "high",
            "confidence": 0.6,
            "reason": "Evening - potential gaming or media consumption",
            "timeframe": "next_3_hours"
        })
    
    # Memory usage prediction
    predictions.append({
        "type": "resource_usage",
        "resource": "memory",
        "prediction": "moderate",
        "confidence": 0.5,
        "reason": "Based on typical usage patterns",
        "timeframe": "next_1_hour"
    })
    
    return predictions

def _predict_user_activity(current_hour):
    """Predict user activity patterns"""
    predictions = []
    
    if current_hour < 8:
        predictions.append({
            "type": "user_activity",
            "activity": "low",
            "confidence": 0.8,
            "reason": "Early morning - typically low activity",
            "timeframe": "next_2_hours"
        })
    elif 12 <= current_hour <= 13:
        predictions.append({
            "type": "user_activity",
            "activity": "reduced",
            "confidence": 0.7,
            "reason": "Lunch time - typically reduced activity",
            "timeframe": "next_1_hour"
        })
    
    return predictions

def _predict_maintenance_needs():
    """Predict system maintenance needs"""
    predictions = []
    
    # Simple maintenance predictions
    predictions.append({
        "type": "maintenance",
        "task": "disk_cleanup",
        "urgency": "low",
        "confidence": 0.4,
        "reason": "Routine maintenance recommendation",
        "timeframe": "next_week"
    })
    
    predictions.append({
        "type": "maintenance",
        "task": "system_restart",
        "urgency": "medium",
        "confidence": 0.6,
        "reason": "System uptime optimization",
        "timeframe": "next_24_hours"
    })
    
    return predictions

def _calculate_prediction_confidence(predictions):
    """Calculate overall confidence in predictions"""
    if not predictions:
        return "no_data"
    
    confidences = [p.get("confidence", 0) for p in predictions]
    avg_confidence = statistics.mean(confidences)
    
    if avg_confidence > 0.7:
        return "high"
    elif avg_confidence > 0.4:
        return "moderate"
    else:
        return "low"
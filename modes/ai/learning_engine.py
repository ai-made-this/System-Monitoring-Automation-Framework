"""Learning Engine - Continuously learns from user behavior and system data"""
import json
import time
from pathlib import Path
from collections import defaultdict, deque
import statistics

DATA_DIR = Path(__file__).parent / "data"
LEARNING_DATA = DATA_DIR / "learning_data.json"
MODEL_STATE = DATA_DIR / "model_state.json"

def get_learning_engine():
    """Get status and insights from the learning engine"""
    try:
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(exist_ok=True)
        
        # Load learning data
        learning_data = _load_learning_data()
        
        # Process recent observations
        insights = _process_learning_data(learning_data)
        
        # Update model state
        model_state = _update_model_state(insights)
        
        return {
            "status": "learning",
            "insights": insights,
            "model_state": model_state,
            "data_points": len(learning_data.get("observations", [])),
            "learning_confidence": _calculate_learning_confidence(learning_data)
        }
    except Exception as e:
        return {"error": str(e)}

def _load_learning_data():
    """Load existing learning data or create new structure"""
    if LEARNING_DATA.exists():
        with open(LEARNING_DATA, 'r') as f:
            return json.load(f)
    else:
        return {
            "observations": [],
            "patterns": {},
            "user_preferences": {},
            "performance_metrics": {},
            "last_updated": time.time()
        }

def _process_learning_data(learning_data):
    """Process learning data to extract insights"""
    observations = learning_data.get("observations", [])
    
    if len(observations) < 5:
        return {
            "status": "insufficient_data",
            "message": "Need more observations to generate insights"
        }
    
    insights = {
        "usage_patterns": _analyze_usage_patterns(observations),
        "performance_trends": _analyze_performance_trends(observations),
        "user_preferences": _extract_user_preferences(observations),
        "optimization_opportunities": _identify_optimizations(observations)
    }
    
    return insights

def _analyze_usage_patterns(observations):
    """Analyze user usage patterns"""
    if not observations:
        return {"message": "No usage data"}
    
    # Analyze time-based patterns
    hourly_usage = defaultdict(int)
    app_usage = defaultdict(int)
    
    for obs in observations[-100:]:  # Last 100 observations
        if "timestamp" in obs:
            hour = time.localtime(obs["timestamp"]).tm_hour
            hourly_usage[hour] += 1
        
        if "active_app" in obs:
            app_usage[obs["active_app"]] += 1
    
    return {
        "peak_hours": sorted(hourly_usage.items(), key=lambda x: x[1], reverse=True)[:5],
        "most_used_apps": sorted(app_usage.items(), key=lambda x: x[1], reverse=True)[:10],
        "usage_consistency": _calculate_consistency(hourly_usage)
    }

def _analyze_performance_trends(observations):
    """Analyze system performance trends"""
    cpu_usage = []
    memory_usage = []
    
    for obs in observations[-50:]:  # Last 50 observations
        if "cpu_usage" in obs:
            cpu_usage.append(obs["cpu_usage"])
        if "memory_usage" in obs:
            memory_usage.append(obs["memory_usage"])
    
    trends = {}
    
    if cpu_usage:
        trends["cpu"] = {
            "average": round(statistics.mean(cpu_usage), 2),
            "trend": "increasing" if len(cpu_usage) > 10 and cpu_usage[-5:] > cpu_usage[:5] else "stable"
        }
    
    if memory_usage:
        trends["memory"] = {
            "average": round(statistics.mean(memory_usage), 2),
            "trend": "increasing" if len(memory_usage) > 10 and memory_usage[-5:] > memory_usage[:5] else "stable"
        }
    
    return trends

def _extract_user_preferences(observations):
    """Extract user preferences from behavior"""
    preferences = {
        "preferred_work_hours": _get_preferred_hours(observations),
        "application_preferences": _get_app_preferences(observations),
        "interaction_style": _analyze_interaction_style(observations)
    }
    
    return preferences

def _identify_optimizations(observations):
    """Identify optimization opportunities"""
    optimizations = []
    
    # Check for repetitive tasks
    if _detect_repetitive_tasks(observations):
        optimizations.append({
            "type": "automation",
            "description": "Repetitive tasks detected - consider macro automation",
            "priority": "medium"
        })
    
    # Check for resource inefficiencies
    if _detect_resource_waste(observations):
        optimizations.append({
            "type": "resource_optimization",
            "description": "Resource usage patterns suggest optimization opportunities",
            "priority": "high"
        })
    
    return optimizations

def _update_model_state(insights):
    """Update the learning model state"""
    model_state = {
        "last_updated": time.time(),
        "learning_phase": _determine_learning_phase(insights),
        "confidence_level": _calculate_model_confidence(insights),
        "active_patterns": len(insights.get("usage_patterns", {}).get("peak_hours", [])),
        "optimization_suggestions": len(insights.get("optimization_opportunities", []))
    }
    
    # Save model state
    with open(MODEL_STATE, 'w') as f:
        json.dump(model_state, f, indent=2)
    
    return model_state

def _calculate_learning_confidence(learning_data):
    """Calculate confidence in learning accuracy"""
    observation_count = len(learning_data.get("observations", []))
    
    if observation_count < 10:
        return "low"
    elif observation_count < 50:
        return "moderate"
    else:
        return "high"

def _calculate_consistency(usage_data):
    """Calculate consistency score for usage patterns"""
    if not usage_data:
        return 0
    
    values = list(usage_data.values())
    if len(values) < 2:
        return 0
    
    # Simple consistency measure based on standard deviation
    std_dev = statistics.stdev(values)
    mean_val = statistics.mean(values)
    
    # Lower std_dev relative to mean indicates higher consistency
    consistency = max(0, 1 - (std_dev / mean_val)) if mean_val > 0 else 0
    return round(consistency, 2)

def _get_preferred_hours(observations):
    """Determine user's preferred working hours"""
    # Simplified implementation
    return {"morning": "9-12", "afternoon": "13-17", "evening": "18-22"}

def _get_app_preferences(observations):
    """Determine application preferences"""
    # Simplified implementation
    return {"productivity": ["notepad", "browser"], "entertainment": ["games", "media"]}

def _analyze_interaction_style(observations):
    """Analyze user interaction style"""
    # Simplified implementation
    return {"style": "efficient", "shortcuts_usage": "high", "multitasking": "moderate"}

def _detect_repetitive_tasks(observations):
    """Detect repetitive task patterns"""
    # Simplified detection logic
    return len(observations) > 20 and len(set(obs.get("action", "") for obs in observations[-10:])) < 3

def _detect_resource_waste(observations):
    """Detect resource waste patterns"""
    # Simplified detection logic
    recent_cpu = [obs.get("cpu_usage", 0) for obs in observations[-10:] if "cpu_usage" in obs]
    return len(recent_cpu) > 5 and statistics.mean(recent_cpu) > 80

def _determine_learning_phase(insights):
    """Determine current learning phase"""
    if not insights or insights.get("status") == "insufficient_data":
        return "initial"
    elif len(insights.get("usage_patterns", {}).get("peak_hours", [])) < 3:
        return "pattern_discovery"
    else:
        return "optimization"

def _calculate_model_confidence(insights):
    """Calculate model confidence level"""
    if not insights or insights.get("status") == "insufficient_data":
        return "low"
    
    pattern_count = len(insights.get("usage_patterns", {}).get("peak_hours", []))
    if pattern_count > 5:
        return "high"
    elif pattern_count > 2:
        return "moderate"
    else:
        return "low"
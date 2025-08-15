"""Pattern Recognition - Identifies patterns in user behavior and system usage"""
import json
import time
from pathlib import Path
from collections import defaultdict
import statistics

DATA_DIR = Path(__file__).parent / "data"
PATTERNS_FILE = DATA_DIR / "recognized_patterns.json"

def get_pattern_recognition():
    """Recognize patterns in user behavior and system usage"""
    try:
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(exist_ok=True)
        
        # Load existing patterns or create new
        if PATTERNS_FILE.exists():
            with open(PATTERNS_FILE, 'r') as f:
                patterns = json.load(f)
        else:
            patterns = {"patterns": [], "last_analysis": None}
        
        # Analyze current patterns
        current_patterns = _detect_current_patterns()
        
        # Update pattern database
        patterns["patterns"].extend(current_patterns)
        patterns["last_analysis"] = time.time()
        
        # Keep only recent patterns (last 30 days)
        cutoff_time = time.time() - (30 * 24 * 3600)
        patterns["patterns"] = [p for p in patterns["patterns"] if p.get("timestamp", 0) > cutoff_time]
        
        # Save updated patterns
        with open(PATTERNS_FILE, 'w') as f:
            json.dump(patterns, f, indent=2)
        
        # Analyze pattern types
        pattern_analysis = _analyze_pattern_types(patterns["patterns"])
        
        return {
            "status": "active",
            "current_patterns": current_patterns,
            "pattern_analysis": pattern_analysis,
            "total_patterns": len(patterns["patterns"]),
            "confidence": _calculate_pattern_confidence(patterns["patterns"])
        }
    except Exception as e:
        return {"error": str(e)}

def _detect_current_patterns():
    """Detect patterns in current system state"""
    current_time = time.time()
    hour = time.localtime(current_time).tm_hour
    
    patterns = []
    
    # Time-based patterns
    if 9 <= hour <= 17:
        patterns.append({
            "type": "work_hours",
            "description": "Activity during typical work hours",
            "timestamp": current_time,
            "confidence": 0.8
        })
    elif 18 <= hour <= 23:
        patterns.append({
            "type": "evening_activity",
            "description": "Evening computer usage",
            "timestamp": current_time,
            "confidence": 0.7
        })
    
    # Add more pattern detection logic here
    # This is a basic implementation - can be expanded with ML models
    
    return patterns

def _analyze_pattern_types(patterns):
    """Analyze types of patterns found"""
    if not patterns:
        return {"message": "No patterns to analyze"}
    
    pattern_types = defaultdict(int)
    confidence_scores = []
    
    for pattern in patterns:
        pattern_types[pattern.get("type", "unknown")] += 1
        confidence_scores.append(pattern.get("confidence", 0))
    
    return {
        "pattern_distribution": dict(pattern_types),
        "most_common_pattern": max(pattern_types.items(), key=lambda x: x[1])[0] if pattern_types else None,
        "average_confidence": round(statistics.mean(confidence_scores), 2) if confidence_scores else 0,
        "pattern_variety": len(pattern_types)
    }

def _calculate_pattern_confidence(patterns):
    """Calculate overall confidence in pattern recognition"""
    if len(patterns) < 10:
        return "low"
    elif len(patterns) < 50:
        return "moderate"
    else:
        return "high"
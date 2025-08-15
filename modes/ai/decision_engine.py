"""Decision Engine - Makes decisions based on analysis and predictions"""
import json
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DECISIONS_FILE = DATA_DIR / "decisions.json"
RULES_FILE = DATA_DIR / "decision_rules.json"

def get_decision_engine():
    """Make decisions based on current system state and predictions"""
    try:
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(exist_ok=True)
        
        # Load decision rules
        rules = _load_decision_rules()
        
        # Make decisions based on current state
        decisions = _make_decisions(rules)
        
        # Save decisions
        decision_data = {
            "decisions": decisions,
            "timestamp": time.time(),
            "rules_applied": len(rules),
            "decision_count": len(decisions)
        }
        
        with open(DECISIONS_FILE, 'w') as f:
            json.dump(decision_data, f, indent=2)
        
        return {
            "status": "active",
            "decisions": decisions,
            "decision_count": len(decisions),
            "rules_loaded": len(rules),
            "last_decision_time": decision_data["timestamp"]
        }
    except Exception as e:
        return {"error": str(e)}

def _load_decision_rules():
    """Load decision-making rules"""
    if RULES_FILE.exists():
        with open(RULES_FILE, 'r') as f:
            return json.load(f)
    else:
        # Create default rules
        default_rules = {
            "resource_management": [
                {
                    "condition": "cpu_usage > 80",
                    "action": "suggest_process_optimization",
                    "priority": "high"
                },
                {
                    "condition": "memory_usage > 85",
                    "action": "suggest_memory_cleanup",
                    "priority": "high"
                },
                {
                    "condition": "disk_usage > 90",
                    "action": "suggest_disk_cleanup",
                    "priority": "critical"
                }
            ],
            "automation": [
                {
                    "condition": "repetitive_task_detected",
                    "action": "suggest_macro_creation",
                    "priority": "medium"
                },
                {
                    "condition": "scheduled_task_ready",
                    "action": "execute_scheduled_task",
                    "priority": "medium"
                }
            ],
            "optimization": [
                {
                    "condition": "low_activity_period",
                    "action": "suggest_maintenance_tasks",
                    "priority": "low"
                }
            ]
        }
        
        with open(RULES_FILE, 'w') as f:
            json.dump(default_rules, f, indent=2)
        
        return default_rules

def _make_decisions(rules):
    """Make decisions based on rules and current state"""
    decisions = []
    current_time = time.time()
    
    # Simulate decision making based on rules
    # In a real implementation, this would check actual system state
    
    for category, rule_list in rules.items():
        for rule in rule_list:
            # Simulate condition checking
            if _evaluate_condition(rule["condition"]):
                decision = {
                    "category": category,
                    "action": rule["action"],
                    "priority": rule["priority"],
                    "reason": f"Rule triggered: {rule['condition']}",
                    "timestamp": current_time,
                    "executed": False
                }
                decisions.append(decision)
    
    return decisions

def _evaluate_condition(condition):
    """Evaluate a decision rule condition"""
    # This is a simplified implementation
    # In reality, this would check actual system metrics
    
    current_hour = time.localtime().tm_hour
    
    # Simulate some conditions
    if "cpu_usage > 80" in condition:
        return current_hour in [10, 11, 14, 15]  # Simulate high CPU during work hours
    elif "memory_usage > 85" in condition:
        return current_hour in [16, 17, 20, 21]  # Simulate high memory usage
    elif "disk_usage > 90" in condition:
        return False  # Rarely trigger disk cleanup
    elif "repetitive_task_detected" in condition:
        return current_hour % 4 == 0  # Simulate detection every 4 hours
    elif "low_activity_period" in condition:
        return current_hour < 8 or current_hour > 22  # Early morning or late night
    
    return False
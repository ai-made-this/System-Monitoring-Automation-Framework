"""Query Processor - Processes natural language queries about system and habits"""
import json
import time
from pathlib import Path
import re

DATA_DIR = Path(__file__).parent / "data"
QUERY_LOG = DATA_DIR / "query_log.json"

def get_query_processor():
    """Process natural language queries about system state and user habits"""
    try:
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(exist_ok=True)
        
        # Get query processing capabilities
        capabilities = _get_query_capabilities()
        
        # Get recent query history
        history = _get_query_history()
        
        return {
            "status": "ready",
            "capabilities": capabilities,
            "recent_queries": history,
            "supported_query_types": _get_supported_query_types()
        }
    except Exception as e:
        return {"error": str(e)}

def _get_query_capabilities():
    """Get query processing capabilities"""
    return {
        "natural_language": {
            "description": "Process natural language questions",
            "examples": [
                "Why is my CPU usage high?",
                "When do I use the most memory?",
                "What apps do I use most often?",
                "Why does my system slow down at 3 PM?"
            ]
        },
        "system_analysis": {
            "description": "Analyze system performance questions",
            "capabilities": ["resource_usage", "performance_trends", "bottleneck_identification"]
        },
        "habit_analysis": {
            "description": "Answer questions about user habits",
            "capabilities": ["usage_patterns", "time_analysis", "application_preferences"]
        },
        "predictive_queries": {
            "description": "Answer predictive questions",
            "examples": [
                "When will I need more storage?",
                "What time should I schedule maintenance?",
                "When am I most productive?"
            ]
        }
    }

def _get_query_history():
    """Get recent query history"""
    if not QUERY_LOG.exists():
        return []
    
    with open(QUERY_LOG, 'r') as f:
        log = json.load(f)
    
    return log.get("queries", [])[-10:]  # Last 10 queries

def _get_supported_query_types():
    """Get supported query types with patterns"""
    return {
        "why_questions": {
            "patterns": ["why is", "why does", "why am"],
            "examples": ["Why is my CPU high?", "Why does Chrome use so much memory?"]
        },
        "when_questions": {
            "patterns": ["when do", "when am", "when is", "what time"],
            "examples": ["When do I use most CPU?", "What time am I most active?"]
        },
        "what_questions": {
            "patterns": ["what is", "what are", "what app", "what process"],
            "examples": ["What is using my CPU?", "What apps do I use most?"]
        },
        "how_questions": {
            "patterns": ["how much", "how often", "how long"],
            "examples": ["How much memory do I typically use?", "How often do I restart?"]
        },
        "comparison_questions": {
            "patterns": ["compare", "vs", "versus", "difference between"],
            "examples": ["Compare my morning vs evening usage", "Chrome vs Firefox memory usage"]
        }
    }

def process_query(query_text):
    """Process a specific query and return analysis"""
    try:
        query_text = query_text.lower().strip()
        
        # Log the query
        _log_query(query_text)
        
        # Determine query type
        query_type = _classify_query(query_text)
        
        # Process based on type
        response = _generate_response(query_text, query_type)
        
        return {
            "query": query_text,
            "query_type": query_type,
            "response": response,
            "confidence": _calculate_response_confidence(query_text, response),
            "timestamp": time.time()
        }
    except Exception as e:
        return {"error": str(e), "query": query_text}

def _classify_query(query_text):
    """Classify the type of query"""
    query_types = _get_supported_query_types()
    
    for query_type, info in query_types.items():
        for pattern in info["patterns"]:
            if pattern in query_text:
                return query_type
    
    return "general"

def _generate_response(query_text, query_type):
    """Generate response based on query type and content"""
    # This is a simplified response generator
    # In a real implementation, this would analyze actual system data
    
    if "cpu" in query_text and query_type == "why_questions":
        return {
            "answer": "High CPU usage detected during work hours (9-17). Primary causes: browser with multiple tabs, background processes, and active applications.",
            "details": {
                "peak_usage_time": "14:00-16:00",
                "main_culprits": ["chrome.exe", "python.exe", "system processes"],
                "recommendation": "Consider closing unused browser tabs and limiting concurrent applications"
            }
        }
    
    elif "memory" in query_text and query_type == "when_questions":
        return {
            "answer": "Memory usage peaks between 10 AM and 4 PM, with highest usage around 2 PM.",
            "details": {
                "peak_time": "14:00",
                "average_peak_usage": "78%",
                "pattern": "Correlates with browser usage and multiple open applications"
            }
        }
    
    elif "app" in query_text and "most" in query_text:
        return {
            "answer": "Most used applications: Chrome (45%), VS Code (20%), File Explorer (15%), Notepad (10%), Others (10%)",
            "details": {
                "daily_usage_hours": {"chrome": 3.6, "vscode": 1.6, "explorer": 1.2},
                "usage_pattern": "Heavy browser usage throughout the day, coding sessions in afternoon"
            }
        }
    
    elif query_type == "when_questions":
        return {
            "answer": "Based on usage patterns, you are most active between 9 AM and 6 PM, with peak productivity around 10-11 AM and 2-3 PM.",
            "details": {
                "peak_hours": ["10:00-11:00", "14:00-15:00"],
                "low_activity": ["12:00-13:00", "17:00-18:00"],
                "pattern_confidence": "high"
            }
        }
    
    else:
        return {
            "answer": "I can help analyze your system usage patterns, resource consumption, and application habits. Try asking specific questions about CPU, memory, applications, or timing patterns.",
            "suggestions": [
                "Why is my CPU usage high?",
                "When do I use the most memory?",
                "What apps do I use most often?",
                "How often do I restart my computer?"
            ]
        }

def _log_query(query_text):
    """Log query for analysis"""
    if QUERY_LOG.exists():
        with open(QUERY_LOG, 'r') as f:
            log = json.load(f)
    else:
        log = {"queries": []}
    
    log["queries"].append({
        "query": query_text,
        "timestamp": time.time()
    })
    
    # Keep only last 100 queries
    log["queries"] = log["queries"][-100:]
    
    with open(QUERY_LOG, 'w') as f:
        json.dump(log, f, indent=2)

def _calculate_response_confidence(query_text, response):
    """Calculate confidence in response accuracy"""
    # Simple confidence calculation based on query specificity
    specific_terms = ["cpu", "memory", "disk", "app", "process", "time", "when", "why", "how"]
    term_count = sum(1 for term in specific_terms if term in query_text.lower())
    
    if term_count >= 3:
        return "high"
    elif term_count >= 2:
        return "medium"
    else:
        return "low"
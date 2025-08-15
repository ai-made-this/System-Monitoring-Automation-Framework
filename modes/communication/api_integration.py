"""API Integration - Connect with external services and APIs"""
import json
import time
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "api_config.json"
LOG_FILE = Path(__file__).parent / "api_calls.json"

def get_api_integration():
    """Get API integration status and capabilities"""
    try:
        # Load API configuration
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
        else:
            config = {
                "apis": {},
                "rate_limits": {},
                "authentication": {}
            }
        
        # Load recent API calls
        if LOG_FILE.exists():
            with open(LOG_FILE, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {"calls": []}
        
        return {
            "status": "ready",
            "configured_apis": list(config["apis"].keys()),
            "recent_api_calls": log_data["calls"][-5:],
            "total_api_calls": len(log_data["calls"]),
            "supported_integrations": {
                "discord": "Send messages to Discord channels",
                "slack": "Post to Slack channels",
                "telegram": "Send Telegram messages",
                "webhooks": "Generic HTTP webhook calls",
                "cloud_storage": "Upload to cloud storage services",
                "monitoring_services": "Send metrics to monitoring platforms"
            },
            "capabilities": {
                "authentication": "OAuth, API keys, tokens",
                "rate_limiting": "Respect API rate limits",
                "retry_logic": "Automatic retry on failures",
                "batch_operations": "Bulk API operations",
                "response_caching": "Cache API responses"
            },
            "use_cases": [
                "Send system alerts to chat platforms",
                "Upload monitoring data to cloud",
                "Trigger external automations",
                "Sync data with external services",
                "Remote system monitoring"
            ]
        }
    except Exception as e:
        return {"error": str(e)}
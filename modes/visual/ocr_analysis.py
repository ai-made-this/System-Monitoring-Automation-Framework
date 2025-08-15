"""OCR Analysis - Optical Character Recognition on screen captures"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "ocr_data"

def get_ocr_analysis():
    """Get OCR analysis capabilities and recent text extractions"""
    try:
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(exist_ok=True)
        
        # Check for recent OCR results
        ocr_files = list(DATA_DIR.glob("*.json"))
        recent_ocr = []
        
        for file in ocr_files[-5:]:  # Last 5 OCR results
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    recent_ocr.append({
                        "filename": file.name,
                        "text_length": len(data.get("text", "")),
                        "confidence": data.get("confidence", 0),
                        "timestamp": data.get("timestamp", 0)
                    })
            except:
                pass
        
        return {
            "status": "ready",
            "recent_ocr_results": recent_ocr,
            "total_ocr_files": len(ocr_files),
            "capabilities": {
                "text_extraction": "Extract text from screenshots",
                "confidence_scoring": "OCR confidence levels",
                "language_detection": "Detect text language",
                "text_regions": "Identify text regions in images",
                "batch_processing": "Process multiple images"
            },
            "supported_languages": ["English", "Spanish", "French", "German", "Chinese"],
            "dependencies": [
                "pip install pytesseract",
                "pip install Pillow",
                "Install Tesseract OCR engine"
            ],
            "note": "OCR functionality requires Tesseract OCR to be installed"
        }
    except Exception as e:
        return {"error": str(e)}
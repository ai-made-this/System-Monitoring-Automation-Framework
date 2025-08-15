"""File Creation Module - Creates files with templates or content"""
import os
from pathlib import Path
import json
from datetime import datetime

def create_file(filepath, content="", template=None, overwrite=False):
    """Create a file with specified content or template"""
    try:
        file_path = Path(filepath)
        
        # Check if file exists and overwrite is False
        if file_path.exists() and not overwrite:
            return {"error": f"File {filepath} already exists. Use overwrite=True to replace."}
        
        # Create directory if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Apply template if specified
        if template:
            templates = {
                "python": f'#!/usr/bin/env python3\n"""\nCreated: {datetime.now().isoformat()}\n"""\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()\n',
                "html": f'<!DOCTYPE html>\n<html>\n<head>\n    <title>New Document</title>\n    <meta charset="UTF-8">\n    <!-- Created: {datetime.now().isoformat()} -->\n</head>\n<body>\n    <h1>Hello World</h1>\n</body>\n</html>',
                "javascript": f'// Created: {datetime.now().isoformat()}\n\nfunction main() {\n    console.log("Hello World");\n}\n\nmain();',
                "css": f'/* Created: {datetime.now().isoformat()} */\n\nbody {\n    font-family: Arial, sans-serif;\n    margin: 0;\n    padding: 20px;\n}',
                "markdown": f'# New Document\n\nCreated: {datetime.now().isoformat()}\n\n## Overview\n\nYour content here...',
                "json": '{\n    "created": "' + datetime.now().isoformat() + '",\n    "data": {}\n}',
                "txt": f'Created: {datetime.now().isoformat()}\n\n'
            }
            content = templates.get(template, content)
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "filepath": str(file_path.absolute()),
            "size_bytes": file_path.stat().st_size,
            "template_used": template,
            "created": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

def get_file_create():
    """Get file creation statistics and available templates"""
    try:
        templates = ["python", "html", "javascript", "css", "markdown", "json", "txt"]
        return {
            "available_templates": templates,
            "function": "create_file(filepath, content='', template=None, overwrite=False)",
            "examples": {
                "basic": "create_file('test.txt', 'Hello World')",
                "template": "create_file('script.py', template='python')",
                "overwrite": "create_file('existing.txt', 'New content', overwrite=True)"
            }
        }
    except Exception as e:
        return {"error": str(e)}
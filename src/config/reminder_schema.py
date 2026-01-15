REMINDER_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "Short reminder title"
        },
        "description": {
            "type": "string",
            "description": "Optional detailed description"
        },
        "datetime": {
            "type": "string",
            "description": "%H:%M:%S"
        },
        "option": {
            "type": "string",
            "enum": ["Today", "Tomorrow", "Daily", "Workdays","Weekend"]
        },
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
        },
        "warning": {
            "type": ["string", "null"],
            "description": "If time is ambiguous or risky"
        }
    },
    "required": ["title", "datetime", "option", "confidence"]
}

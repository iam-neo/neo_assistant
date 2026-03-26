import urllib.request
import urllib.error
import json
from typing import Tuple

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

SYSTEM_PROMPT = """You are the natural language intent parser for an AI assistant.
Your job is to read the user's input (which may be in English, Nepali, or heavily mixed) and extract exactly two pieces of information:
1. The 'intent' (must be exactly one of: 'open_app', 'create_folder', 'open_website', 'exit', or 'unknown')
2. The 'data' (the target application, website, folder name, etc. If none, leave it empty).

Rules:
- You MUST output exactly two lines.
- Format:
intent: <intent>
data: <data>
- "open chrome" -> intent: open_app, data: chrome
- "youtube हेर्न मन लाग्यो" -> intent: open_website, data: youtube
- "folder बनाइदेउ test" -> intent: create_folder, data: test
- "exit the assistant" -> intent: exit, data: 
- If you cannot map the request to the supported intents, return "intent: unknown" and "data: ".
- Do NOT output any conversational text, ONLY the two lines requested.
"""

def query_llm(user_input: str) -> Tuple[str, str]:
    """
    Sends the user input to the local Ollama LLM as a fallback parser.
    Returns a tuple of (intent, data).
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{SYSTEM_PROMPT}\n\nUser Input: {user_input}\nOutput:",
        "stream": False,
        "options": {
            "temperature": 0.0 # Force deterministic output
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            response_text = result.get('response', '').strip()
            
            # Parse the strict two-line output
            lines = response_text.split('\n')
            intent = "unknown"
            data_val = ""
            
            for line in lines:
                line = line.strip()
                if line.lower().startswith("intent:"):
                    # Extract intent and clean it
                    intent_str = line.split(":", 1)[1].strip().lower()
                    if intent_str in ["open_app", "create_folder", "open_website", "exit"]:
                        intent = intent_str
                elif line.lower().startswith("data:"):
                    # Extract data and clean it
                    data_val = line.split(":", 1)[1].strip()
                    
            # Normalize empty data to None for consistency with existing parser
            if not data_val:
                data_val = None
                
            return (intent, data_val)
            
    except (urllib.error.URLError, json.JSONDecodeError, Exception) as e:
        # If the LLM is offline or returns a malformed response, fallback gracefully
        # print(f"[DEBUG] LLM parsing failed: {e}") # Optional debug logging
        return ("unknown", None)

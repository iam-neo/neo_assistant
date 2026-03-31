import urllib.request
import urllib.error
import json
from typing import Tuple

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

# Strict system prompt engineered for natural language fallback parsing.
# Heavily optimized to extract correct intents and data targets from English and Nepali commands.
SYSTEM_PROMPT = """You are the natural language intent parser for an AI assistant.
Your job is to read the user's input (in English, Nepali, or heavily mixed) and extract exactly two pieces of information:
1. The 'intent' (MUST be exactly one of: 'open_app', 'create_folder', 'open_website', 'exit', or 'unknown')
2. The 'data' (the target application, website name, or folder name. If none, leave it empty).

Rules:
- You MUST output exactly two lines. No markdown, no explanations, no chatting.
- Format strictly as:
intent: <intent>
data: <data>

Examples:
- "open chrome" -> intent: open_app, data: chrome
- "youtube हेर्न मन लाग्यो" -> intent: open_website, data: youtube
- "folder बनाइदेउ test" -> intent: create_folder, data: test
- "create a folder called test123" -> intent: create_folder, data: test123
- "can you open chrome for me" -> intent: open_app, data: chrome
- "chrome खोलिदेउ" -> intent: open_app, data: chrome
- "word खोल्न पर्यो" -> intent: open_app, data: word
- "facebook मा जाउ" -> intent: open_website, data: facebook
- "exit the assistant" -> intent: exit, data: 
- "bida hau" -> intent: exit, data:
- "I want to watch netflix" -> intent: open_website, data: netflix

If you cannot map the request to the supported intents, return "intent: unknown" and "data: ".
Do NOT output any conversational text, ONLY the two lines requested.
"""

def query_llm(user_input: str) -> Tuple[str, str]:
    """
    Sends the user input to the local Ollama LLM to be parsed.
    This acts as a smart fallback if rule-based parsing fails.
    Returns: A tuple (intent, data).
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{SYSTEM_PROMPT}\n\nUser Input: {user_input}\nOutput:",
        "stream": False,
        "options": {
            "temperature": 0.0 # Force deterministic and structured output
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            response_text = result.get('response', '').strip()
            
            # Parse the strictly formatted two-line output
            lines = response_text.split('\n')
            intent = "unknown"
            data_val = ""
            
            for line in lines:
                line = line.strip()
                if line.lower().startswith("intent:"):
                    # Extract the intent string and clean it up
                    intent_str = line.split(":", 1)[1].strip().lower()
                    if intent_str in ["open_app", "create_folder", "open_website", "exit"]:
                        intent = intent_str
                elif line.lower().startswith("data:"):
                    # Extract the data string
                    data_val = line.split(":", 1)[1].strip()
                    
            # Normalize empty data to None, matching the existing parser behavior
            if not data_val or data_val.lower() == "none":
                data_val = None
                
            return (intent, data_val)
            
    except (urllib.error.URLError, json.JSONDecodeError, Exception) as e:
        # LLM fallback returns unknown intent quietly if offline or if it malfunctions
        # print(f"[DEBUG] LLM fallback error: {e}")
        return ("unknown", None)

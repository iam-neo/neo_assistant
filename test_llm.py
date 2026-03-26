import sys
import os
import io

# Force UTF-8 output for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# Ensure the parent folders are easily accessible for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.parser import parse_command

import unittest.mock
import json

def mock_urlopen(req, timeout=10):
    class MockResponse:
        def __init__(self, data):
            self.data = data
        def read(self):
            return self.data
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
            
    payload = json.loads(req.data.decode('utf-8'))
    prompt = payload.get('prompt', '')
    
    # Mock responses based on input
    if "youtube हेर्न मन लाग्यो" in prompt:
        resp = {"response": "intent: open_website\ndata: youtube"}
    elif "I want to watch youtube" in prompt:
        resp = {"response": "intent: open_website\ndata: youtube"}
    else:
        resp = {"response": "intent: unknown\ndata: none"}
        
    return MockResponse(json.dumps(resp).encode('utf-8'))

def run_tests():
    test_cases = [
        # English fallback (no 'open' keyword to bypass rule-based)
        "I want to watch youtube",
        # Nepali fallback
        "youtube हेर्न मन लाग्यो",
        # Parameter test
        "create a folder called test123",
        # Core intents
        "exit the assistant"
    ]

    print("--- Running Test Cases ---")
    for tc in test_cases:
        print(f"\nUser Input: {tc}")
        intent, data = parse_command(tc)
        print(f"-> Parsed Intent: {intent}")
        print(f"-> Parsed Data:   {data}")

if __name__ == "__main__":
    with unittest.mock.patch('urllib.request.urlopen', side_effect=mock_urlopen):
        run_tests()

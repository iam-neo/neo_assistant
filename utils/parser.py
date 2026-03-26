import re
from typing import Tuple
from utils.llm import query_llm

# --- Phase 2: NLP Normalization Layer ---
# Maps Nepali words (Devanagari & Romanized) and English fillers to core structured tokens.
NORMALIZATION_MAP = {
    # Open / Launch variations
    "खोल": "open",
    "khola": "open",
    "khol": "open",
    "chalao": "open",
    "जाउ": "open",
    "jau": "open",
    "start": "open",
    "launch": "open",
    
    # Create / Folder variations
    "बनाउ": "create",
    "banao": "create",
    "bana": "create",
    "फोल्डर": "folder",
    "naya": "create",
    
    # Exit / Stop
    "बन्द": "exit",
    "banda": "exit",
    "stop": "exit",
    "quit": "exit",
    "close": "exit",

    # Fillers/Politeness (Map to empty string to remove them cleanly)
    "please": "",
    "can you": "",
    "gara": "", 
    "gar": "",
    "the": "",
    "a": "",
    "an": "",
    "ma": ""  # e.g., "youtube ma jau" -> "youtube jau" -> "youtube open"
}

KNOWN_WEBSITES = {"youtube", "google", "github", "stackoverflow", "gmail"}

def normalize_text(text: str) -> str:
    """
    Translates mixed input into a clean, normalized English base sequence.
    Example: 'please chrome khola' -> 'chrome open'
    """
    text = text.lower()
    
    # Sort keys by length descending to match multi-word phrases first
    sorted_keys = sorted(NORMALIZATION_MAP.keys(), key=len, reverse=True)
    
    for word in sorted_keys:
        replacement = NORMALIZATION_MAP[word]
        # Regex \b ensures we only replace whole English/Roman words.
        # Devanagari chars [\u0900-\u097F] don't perfectly align with \b, so we use replace()
        if re.search(r'[\u0900-\u097F]', word): 
            text = text.replace(word, replacement)
        else:
            pattern = r'\b' + re.escape(word) + r'\b'
            text = re.sub(pattern, replacement, text)
            
    # Clean up double spaces created by removing filler words
    return " ".join(text.split())

def parse_command(user_input: str) -> Tuple[str, str]:
    """
    Phase 2 Parser: 
    1. Normalizes input (Nepali -> English, strips fillers)
    2. Uses structured regex/logic to accurately extract intents and targets.
    
    Returns: (intent, data)
    """
    normalized = normalize_text(user_input)
    
    if not normalized:
        return query_llm(user_input)

    # 1. High-priority Exit intent
    if "exit" in normalized:
        return ("exit", None)

    # 2. Structured Create Folder logic
    # Covers "create folder test", "test folder create"
    if "create folder" in normalized or "folder create" in normalized:
        words = normalized.split()
        # The target is any word that isn't 'create' or 'folder'
        target_words = [w for w in words if w not in ["create", "folder"]]
        target = " ".join(target_words).strip()
        
        # Default name if user just says "folder banao" without a name
        return ("create_folder", target if target else "new_folder")

    # 3. Structured Open intent
    if "open" in normalized:
        words = normalized.split()
        target_words = [w for w in words if w != "open"]
        target = " ".join(target_words).strip()
        
        if not target:
            return query_llm(user_input)
            
        # Map target to a website or a system application
        if target in KNOWN_WEBSITES or "." in target:
            return ("open_website", target)
        else:
            return ("open_app", target)

    return query_llm(user_input)

import spacy
from typing import Tuple

try:
    # Load the lightweight English model for basic NLP 
    # (Tokenization, lemmatization, dependency parsing)
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("[!] spaCy English model 'en_core_web_sm' not found.")
    print("[!] Please run: python -m spacy download en_core_web_sm")
    nlp = None

# Mapping common intents to their variations (English + Romanized Nepali + Devanagari)
INTENTS = {
    "open": [
        "open", "start", "launch", "khola", "kholna", "chalao", "chalauna", 
        "khol", "खोल", "चलाउ", "jau", "जाउ", "visit", "browse", "run"
    ],
    "create_folder": [
        "create folder", "make folder", "folder banao", "folder bana", 
        "naya folder", "फोल्डर बनाउ", "build folder", "directory banao", "create a folder"
    ],
    "exit": [
        "exit", "quit", "close", "stop", "banda", "banda gara", "roka", 
        "बन्द", "terminate"
    ]
}

# Common Nepali and English filler/stop words to ignore during parsing
STOP_WORDS = {
    "to", "the", "a", "an", "please", "gara", "up", "ma", "ko", "lai", 
    "bata", "gari", "dinus", "gar", "for", "me", "एउटा", "कृपया", "गर"
}

# Known web domains that should route to the open_website command
KNOWN_WEBSITES = {"youtube", "google", "github", "stackoverflow", "gmail", "facebook", "reddit", "twitter"}


def parse_command(user_input: str) -> Tuple[str, str]:
    """
    Parses user input utilizing lightweight NLP (spaCy) to handle syntactic variations 
    in both English and mixed Nepali expressions. 
    Maintains backward compatibility with simple rule-based intents.
    """
    user_input = user_input.strip().lower()

    if not user_input:
        return ("unknown", None)

    # 1. Exit/Quit Intent (Fast Exact Phrase Match)
    for trigger in INTENTS["exit"]:
        if trigger in user_input:
            return ("exit", None)

    # 2. Create Folder Intent (Phrase Match)
    for trigger in INTENTS["create_folder"]:
        if trigger in user_input:
            # Extract the target string by stripping the trigger
            target = user_input.replace(trigger, "").strip()
            # Clean up trailing/leading stop words (e.g., "folder banao test ko" -> "test")
            words = [w for w in target.split() if w not in STOP_WORDS]
            target = " ".join(words).strip()
            return ("create_folder", target)

    # 3. Flexible NLP parsing for App/Website launching
    target_words = []
    has_open_intent = False

    if nlp:
        # Utilize spaCy to tokenize and lemmatize
        doc = nlp(user_input)
        
        for token in doc:
            word_str = token.text
            lemma_str = token.lemma_

            # Check if the text or root verb matches our open intents
            if word_str in INTENTS["open"] or lemma_str in INTENTS["open"]:
                has_open_intent = True
            elif word_str not in STOP_WORDS and not token.is_punct:
                # If it's not the intent trigger and not a stop word, it's the target noun
                target_words.append(word_str)
    else:
        # Fallback if spaCy isn't installed: simple split matching (legacy behavior)
        words = user_input.split()
        for word in words:
            if word in INTENTS["open"]:
                has_open_intent = True
            elif word not in STOP_WORDS:
                target_words.append(word)

    # If we detected an "open" action, route it properly
    if has_open_intent:
        target = " ".join(target_words).strip()
        
        if not target:
            return ("unknown", None)
            
        # Heuristics to separate websites from local apps
        if target in KNOWN_WEBSITES or "." in target:
            return ("open_website", target)
        else:
            return ("open_app", target)

    # 4. Fallback: Unknown intent
    return ("unknown", None)

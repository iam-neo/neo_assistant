def parse_command(user_input: str) -> tuple:
    """
    Parses the user input to detect intent and extract the relevant data payload.
    This uses a simple rule-based system instead of heavy AI.
    
    Returns:
        tuple: (intent_name, data)
    """
    # Clean up the input string
    user_input = user_input.strip().lower()

    # Rule 1: Exit/Quit commands
    if user_input in ["exit", "quit", "close", "stop"]:
        return ("exit", None)

    # Rule 2: Open an application or website
    elif user_input.startswith("open "):
        # Extract the target string (e.g., "chrome", "youtube", "notepad")
        target = user_input.replace("open ", "", 1).strip()
        
        # Determine if the target is a website based on simple heuristics
        # (Contains a dot like .com, or is a well-known site name)
        known_websites = ["youtube", "google", "github", "stackoverflow", "gmail"]
        if "." in target or target in known_websites:
            return ("open_website", target)
        else:
            return ("open_app", target)

    # Rule 3: Create a folder
    elif user_input.startswith("create folder ") or user_input.startswith("make folder "):
        # Remove the command trigger to get just the target folder name
        trigger = "create folder " if user_input.startswith("create folder ") else "make folder "
        folder_name = user_input.replace(trigger, "", 1).strip()
        return ("create_folder", folder_name)

    # Fallback: Unknown intent
    else:
        return ("unknown", None)

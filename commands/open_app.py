import os
import json

def execute(app_name: str):
    """
    Opens a standard system application based on the user's intent.
    Uses apps.json to map conversational app names to system commands.
    """
    print(f"[*] Attempting to open application: '{app_name}'...")

    # Build an absolute path to the data/apps.json file
    data_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "apps.json")
    
    try:
        # Load the predefined apps
        with open(data_file_path, "r") as f:
            known_apps = json.load(f)
            
        # Get the executable command, default to the user's string if not explicitly defined
        system_command = known_apps.get(app_name, app_name)
        
        # On Windows, using the 'start' command handles PATH resolution smoothly
        result = os.system(f"start {system_command}")
        
        if result == 0:
            print(f"[+] Successfully launched '{app_name}'.")
        else:
            print(f"[-] Could not find or launch application: '{app_name}'.")
            
    except FileNotFoundError:
        print("[!] Error: data/apps.json configuration file not found.")
    except Exception as e:
        print(f"[!] An error occurred while opening the application: {str(e)}")

import os

def execute(folder_name: str):
    """
    Creates a new directory in the current working environment.
    """
    print(f"[*] Attempting to create folder: '{folder_name}'...")
    
    # Handle empty folder names gracefully
    if not folder_name:
        print("[-] Error: No folder name was provided.")
        return

    try:
        # exist_ok=False ensures we know if it already exists to alert the user
        os.makedirs(folder_name, exist_ok=False)
        print(f"[+] Folder '{folder_name}' created successfully in {os.getcwd()}")
    except FileExistsError:
        print(f"[-] A folder with the name '{folder_name}' already exists.")
    except PermissionError:
        print(f"[!] Permission denied: Cannot create a folder here.")
    except Exception as e:
        print(f"[!] An unexpected error occurred while creating the folder: {str(e)}")

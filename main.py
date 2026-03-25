import sys
import os

# Ensure the parent folders are easily accessible for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the parser
from utils.parser import parse_command

# Import command actions
from commands.open_app import execute as execute_open_app
from commands.open_website import execute as execute_open_website
from commands.create_folder import execute as execute_create_folder

class NeoAssistant:
    def __init__(self):
        # State variable for the main loop
        self.running = True

    def display_welcome_banner(self):
        """Displays a simple, clean UI welcome banner."""
        print("="*50)
        print(" " * 12 + "🤖 Neo Assistant (Offline)")
        print("="*50)
        print(" Hello! I am your local AI assistant.")
        print(" Available intents:")
        print("  - Open applications -> 'open chrome', 'open notepad'")
        print("  - Open websites -> 'open youtube'")
        print("  - Create folders -> 'create folder my_test_folder'")
        print("  - Quit -> 'exit'\n")

    def run(self):
        """Starts the interactive input loop."""
        self.display_welcome_banner()

        while self.running:
            try:
                # Capture user input
                user_input = input("Neo> ")
                
                # Check for empty input and skip
                if not user_input.strip():
                    continue

                # 1. Parse intent
                intent, data = parse_command(user_input)

                # 2. Route intent to the modular executor functions
                if intent == "open_app":
                    execute_open_app(data)
                elif intent == "open_website":
                    execute_open_website(data)
                elif intent == "create_folder":
                    execute_create_folder(data)
                elif intent == "exit":
                    print("[+] Shutting down Neo Assistant. Goodbye!")
                    self.running = False
                else:
                    print("[-] Unknown command. I didn't quite understand that.")
                    print("    Try 'open chrome' or 'create folder example'.")
                    
            except KeyboardInterrupt:
                # Graceful termination via Ctrl+C
                print("\n[+] Shutting down Neo Assistant. Goodbye!")
                self.running = False
            except Exception as e:
                # Top-level exception handling to prevent the loop from crashing
                print(f"[!] A system error occurred: {str(e)}")

# Script execution entry point
if __name__ == "__main__":
    assistant = NeoAssistant()
    assistant.run()

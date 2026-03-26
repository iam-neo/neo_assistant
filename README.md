# Neo Assistant

A lightweight, rule-based local AI assistant written purely in Python. Neo Assistant is designed to be fully modular and run entirely offline without requiring heavy LLMs or external dependencies. It takes text commands, interprets the user's intent via a straightforward parsing rule-engine, and executes system-level operations.

## Features

- **Open Applications:** Start your favorite desktop apps like Chrome or Notepad instantly.
- **Open Websites:** Launch any website directly in your default browser.
- **Create Folders:** Instantly make new directories on your filesystem.
- **Mixed Language NLP (Phase 2):** Native support for English and Nepali commands using a lightweight normalization layer.
- **LLM Fallback (Phase 3):** Integrates with a local Ollama instance (`mistral` model) to handle complex reasoning entirely offline when rule-based engines fail.
- **Extensible & Modular Architecture:** Commands are cleanly separated into their own modules, making it incredibly easy to add new capabilities.
- **100% Offline:** Zero external tracking. Uses standard Python libraries and local machine-learning models.

## Project Structure

```text
neo_assistant/
│── main.py                   # The main interactive loop and command router
│── commands/                 # Directory containing all actionable command modules
│     ├── open_app.py         # Module to launch desktop applications using system triggers
│     ├── create_folder.py    # Module to safely make directories
│     └── open_website.py     # Module to open URLs dynamically
│── utils/                    
│     ├── parser.py           # The rule-based intent parsing engine
│     └── llm.py              # LLM Connector communicating with local Ollama
└── data/
      └── apps.json           # JSON configuration mapping app names to system commands
```

## Setup & Installation

Because Neo Assistant demands zero external dependencies, the setup is practically instantaneous.

1. Download or clone this project locally.
2. Ensure you have **Python 3.x** installed on your system.
3. Tweak your applications mapping list inside `data/apps.json` to configure the paths to your favorite tools.

## Usage

Navigate to the project folder via your terminal and run the main entry point:

```bash
python main.py
```

### Supported Flow

Neo Assistant evaluates continuous user inputs. Below are examples of queries you can issue once the `Neo>` prompt appears:

- **Launch an application:** `open chrome`, `open notepad`, `open calculator`
- **Navigate to a URL:** `open youtube`, `open github.com`, `open stackoverflow`
- **Create a directory:** `create folder new_project_folder`
- **Stop the assistant:** `exit`, `quit`, or `close`

## Extending the Assistant

If you want to add a new trick to Neo Assistant:
1. Create a new `.py` file inside the `commands/` directory carrying an `execute(data)` function.
2. Update the `parse_command` logic inside `utils/parser.py` to identify your new intent.
3. Import and route your new command inside the `run()` loop in `main.py`.

That's it!

## License

This project was built to be lightweight and scalable. Feel free to fork it, modify it, extend it with ML capabilities, or use it for your own automations.

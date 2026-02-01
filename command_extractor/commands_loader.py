import os
import tomllib

def load_commands(commands_dir="/data/data/com.termux/files/home/.gemini/commands"):
    commands = {}
    if not os.path.exists(commands_dir):
        return commands
    
    for filename in os.listdir(commands_dir):
        if filename.endswith(".toml"):
            command_name = filename[:-5]
            file_path = os.path.join(commands_dir, filename)
            try:
                with open(file_path, "rb") as f:
                    data = tomllib.load(f)
                    commands[command_name] = {
                        "description": data.get("description", ""),
                        "prompt": data.get("prompt", "")
                    }
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return commands

if __name__ == "__main__":
    cmds = load_commands()
    for name, info in cmds.items():
        print(f"Command: {name} - {info['description']}")

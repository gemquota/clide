import os

def save_new_command(name, description, prompt, commands_dir="/data/data/com.termux/files/home/.gemini/commands"):
    if not os.path.exists(commands_dir):
        os.makedirs(commands_dir, exist_ok=True)
    
    file_path = os.path.join(commands_dir, f"{name}.toml")
    
    # Simple TOML formatter
    content = f'description = "{description}"\n'
    content += f'prompt = """\n{prompt}\n"""\n'
    
    with open(file_path, "w") as f:
        f.write(content)
    
    print(f"Command '{name}' saved to {file_path}")
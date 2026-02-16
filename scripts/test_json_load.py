import json

path = "swarm/commands/vector_registry.json"
try:
    with open(path, "r") as f:
        data = json.load(f)
    print(f"Successfully loaded {len(data)} items.")
except json.JSONDecodeError as e:
    print(f"JSON Error: {e}")
    print(f"Pos: {e.pos}")
    print(f"Line: {e.lineno}, Col: {e.colno}")
    with open(path, "r") as f:
        f.seek(max(0, e.pos - 50))
        context = f.read(100)
        print(f"Context: {repr(context)}")
except Exception as e:
    print(f"General Error: {e}")

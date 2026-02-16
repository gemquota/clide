import json
import os

path = "swarm/commands/vector_registry.json"
try:
    with open(path, "r") as f:
        # Read the file until the error position
        # line 152236, column 19
        for i in range(152235):
            f.readline()
        line = f.readline()
        print(f"Line 152236: {repr(line)}")
        next_line = f.readline()
        print(f"Line 152237: {repr(next_line)}")
except Exception as e:
    print(f"Error: {e}")

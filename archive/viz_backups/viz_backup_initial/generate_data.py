import csv
import json
import os
import math

def generate_graph_data(csv_path, output_path):
    nodes = []
    links = []
    
    tags_map = {} # tag_name -> count
    commands_data = []

    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    try:
        # Pass 1: Count tags and collect commands
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cmd_name = row['Command'].strip()
                if not cmd_name:
                    continue
                
                try:
                    occurrences = int(row['Occurrences'])
                except ValueError:
                    occurrences = 1
                
                raw_tags = row['Tags']
                tags = [t.strip().lower() for t in raw_tags.split(',')] if raw_tags else []
                tags = [t for t in tags if t] # filter empty
                
                if not tags:
                    tags = ["uncategorized"]

                # Count tags
                for tag in tags:
                    tags_map[tag] = tags_map.get(tag, 0) + 1
                
                commands_data.append({
                    "name": cmd_name,
                    "occurrences": occurrences,
                    "tags": tags,
                    "description": row['Primary Description'],
                    "primary_tag": tags[0]
                })

        # Calculate max occurrences for node scaling logic (if needed)
        # max_occ = max(c["occurrences"] for c in commands_data) if commands_data else 1

        # Pass 2: Build Nodes and Links
        existing_node_ids = set()

        # Command Nodes
        for cmd in commands_data:
            # Scale value: Logarithmic scale is usually better for visualization than linear if variance is high
            # Base size 1 + log(occurrences)
            val = 1 + math.log(cmd["occurrences"] + 1) * 2

            nodes.append({
                "id": cmd["name"],
                "name": cmd["name"],
                "val": val, 
                "group": cmd["primary_tag"],
                "type": "command",
                "description": cmd["description"],
                "tags": cmd["tags"]
            })
            existing_node_ids.add(cmd["name"])

            for tag in cmd["tags"]:
                tag_id = f"tag:{tag}"
                
                # Link Weight Logic
                # Common tags (high count) -> Thinner lines (low weight)
                # Rare tags (low count) -> Thicker lines (high weight)
                tag_count = tags_map.get(tag, 1)
                
                # Weight formula: Inverse to count. 
                # If tag has 1 command, weight 1.0. 
                # If tag has 100 commands, weight 0.1.
                weight = 1.0 / (math.log(tag_count + 1) + 0.5)

                links.append({
                    "source": cmd["name"],
                    "target": tag_id,
                    "value": weight
                })

        # Tag Nodes
        for tag, count in tags_map.items():
            tag_id = f"tag:{tag}"
            
            # Tag size based on how many commands it has
            val = 0.5 + math.log(count + 1)

            nodes.append({
                "id": tag_id,
                "name": tag,
                "val": val,
                "group": "tag", # specific group for styling if needed
                "type": "tag",
                "description": f"Tag used by {count} commands."
            })

        graph_data = {
            "nodes": nodes,
            "links": links
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2)
        
        print(f"Graph data generated at {output_path}")
        print(f"Nodes: {len(nodes)}, Links: {len(links)}")

    except Exception as e:
        print(f"Error generating graph data: {e}")

if __name__ == "__main__":
    CSV_PATH = "ingestion_logs/commands.csv"
    OUTPUT_PATH = "viz/graph_data.json"
    generate_graph_data(CSV_PATH, OUTPUT_PATH)
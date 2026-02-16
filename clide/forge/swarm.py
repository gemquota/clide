import os
import re
import yaml
import json
import sys

# Ensure clide_src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clide import vector_registry

BASE_DIR = "/data/data/com.termux/files/home/openclaw/meta/swarm/new/plugins"
ROOT_MD_DIR = "/data/data/com.termux/files/home/openclaw/meta/swarm/new"

def extract_frontmatter(content):
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)), content[match.end():]
        except yaml.YAMLError:
            pass
    return {}, content

def ingest_agent(plugin_name, agent_file):
    agent_id = os.path.basename(agent_file).replace(".md", "")
    full_id = f"agent:{plugin_name}:{agent_id}"
    
    with open(agent_file, "r") as f:
        content = f.read()
    
    metadata, body = extract_frontmatter(content)
    desc = metadata.get("description", "")
    
    text_for_embedding = f"Agent: {agent_id}\nPlugin: {plugin_name}\nDescription: {desc}\n{body[:500]}"
    
    registry_metadata = {
        "type": "agent",
        "plugin": plugin_name,
        "name": agent_id,
        "description": desc,
        "path": agent_file.replace("/data/data/com.termux/files/home/openclaw/meta/", "")
    }
    
    print(f"Ingesting Agent: {full_id}")
    vector_registry.add_to_registry(full_id, registry_metadata, text_for_embedding)

def ingest_command(plugin_name, command_file):
    cmd_id = os.path.basename(command_file).replace(".md", "")
    full_id = f"command:{plugin_name}:{cmd_id}"
    
    with open(command_file, "r") as f:
        content = f.read()
    
    metadata, body = extract_frontmatter(content)
    desc = metadata.get("description", "")
    
    text_for_embedding = f"Command: {cmd_id}\nPlugin: {plugin_name}\nDescription: {desc}\n{body[:500]}"
    
    registry_metadata = {
        "type": "command",
        "plugin": plugin_name,
        "name": cmd_id,
        "description": desc,
        "path": command_file.replace("/data/data/com.termux/files/home/openclaw/meta/", "")
    }
    
    print(f"Ingesting Command: {full_id}")
    vector_registry.add_to_registry(full_id, registry_metadata, text_for_embedding)

def ingest_skill(plugin_name, skill_dir):
    skill_id = os.path.basename(skill_dir)
    full_id = f"skill:{plugin_name}:{skill_id}"
    skill_file = os.path.join(skill_dir, "SKILL.md")
    
    if not os.path.exists(skill_file):
        return

    with open(skill_file, "r") as f:
        content = f.read()
    
    metadata, body = extract_frontmatter(content)
    desc = metadata.get("description", "")
    
    text_for_embedding = f"Skill: {skill_id}\nPlugin: {plugin_name}\nDescription: {desc}\n{body[:500]}"
    
    registry_metadata = {
        "type": "skill",
        "plugin": plugin_name,
        "name": skill_id,
        "description": desc,
        "path": skill_file.replace("/data/data/com.termux/files/home/openclaw/meta/", "")
    }
    
    print(f"Ingesting Skill: {full_id}")
    vector_registry.add_to_registry(full_id, registry_metadata, text_for_embedding)

def ingest_general_md(file_path, category="general"):
    file_name = os.path.basename(file_path).replace(".md", "")
    full_id = f"doc:{category}:{file_name}"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    metadata, body = extract_frontmatter(content)
    desc = metadata.get("description", body[:200].strip().replace("\n", " "))
    
    text_for_embedding = f"Document: {file_name}\nCategory: {category}\nDescription: {desc}\n{body[:1000]}"
    
    registry_metadata = {
        "type": "doc",
        "category": category,
        "name": file_name,
        "description": desc,
        "path": file_path.replace("/data/data/com.termux/files/home/openclaw/meta/", "")
    }
    
    print(f"Ingesting Document: {full_id}")
    vector_registry.add_to_registry(full_id, registry_metadata, text_for_embedding)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--skip", type=int, default=0)
    parser.add_argument("--docs-only", action="store_true")
    args = parser.parse_args()

    if args.docs_only:
        # Ingest root MDs
        for f in os.listdir(ROOT_MD_DIR):
            if f.endswith(".md"):
                ingest_general_md(os.path.join(ROOT_MD_DIR, f), category="swarm-core")
        return

    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    all_plugins = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))])
    
    plugins_to_process = all_plugins[args.skip : args.skip + args.batch_size]
    
    total = len(all_plugins)
    processed = args.skip
    
    print(f"Starting batch ingestion: {processed} to {processed + len(plugins_to_process)} of {total}")

    for plugin in plugins_to_process:
        plugin_path = os.path.join(BASE_DIR, plugin)
        print(f"--- Processing Plugin: {plugin} ---")
        
        # Ingest Plugin README
        readme_path = os.path.join(plugin_path, "README.md")
        if os.path.exists(readme_path):
            ingest_general_md(readme_path, category=f"plugin:{plugin}")

        # Ingest Agents
        agents_dir = os.path.join(plugin_path, "agents")
        if os.path.exists(agents_dir):
            for f in sorted(os.listdir(agents_dir)):
                if f.endswith(".md"):
                    ingest_agent(plugin, os.path.join(agents_dir, f))
        
        # Ingest Commands
        commands_dir = os.path.join(plugin_path, "commands")
        if os.path.exists(commands_dir):
            for f in sorted(os.listdir(commands_dir)):
                if f.endswith(".md"):
                    ingest_command(plugin, os.path.join(commands_dir, f))
        
        # Ingest Skills
        skills_dir = os.path.join(plugin_path, "skills")
        if os.path.exists(skills_dir):
            for d in sorted(os.listdir(skills_dir)):
                skill_path = os.path.join(skills_dir, d)
                if os.path.isdir(skill_path):
                    ingest_skill(plugin, skill_path)
        
        processed += 1
        print(f"Progress: {processed}/{total} plugins processed.")

if __name__ == "__main__":
    main()
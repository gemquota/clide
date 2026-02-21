# FORGE // SKILL

Synthesizes a new modular capability (Agent Skill) for the system.

## Usage
`./cli forge skill <name> [description]`

## Description
This command creates a new directory in `swarm/skills/` with a `SKILL.md` template and an `__init__.py` file. This allows the system to discover and activate the new skill during autonomous workflows.

<card>
Title: SKILL ARCHITECTURE
Root: swarm/skills/
Components: SKILL.md, __init__.py
Registry: Indexed in 768D (memory.db)
</card>

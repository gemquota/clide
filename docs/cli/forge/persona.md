# FORGE // PERSONA

Defines a new system-prompt identity (Persona) for the agent.

## Usage
`./cli forge persona <name> <description> <directive>`

## Description
This command creates a `.toml` configuration file in `swarm/personas/` defining a unique identity with specific operational directives. These personas can be swapped to change the agent's behavior, tone, and focus.

<card>
Title: PERSONA DEFINITION
Format: TOML
Location: swarm/personas/
Fields: name, description, directive
</card>

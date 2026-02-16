# FORGE TOOL

## Tier: Basic
- Generates PEP 723 compatible Python code.
- Includes automatic dependency detection.
- Injects the latest 10 project facts for context-aware logic.
Usage: ./cli forge tool <name> <prompt>

## Tier: More
- Generates PEP 723 compatible Python code.
- Includes automatic dependency detection.
- Injects the latest 10 project facts for context-aware logic.
Usage: ./cli forge tool <name> <prompt>

TECHNICAL DEEP-DIVE:
The 'tool' command is the 'Production Factory' of CLIDE.
1. Intelligence: Sends the user prompt to 'gemini-2.0-flash'.
2. Templating: Applies the 'mcp_generator.get_python_mcp_template'.
3. Facts: Fetches top 10 facts using 'clide.brain.memory.get_extracted_facts'.
4. Verification: Triggers 'forge test' automatically before indexing.
5. Result: A functional, indexed MCP server ready for use in the Gemini CLI.
Primary Directory: swarm/commands/mcp_servers/.

## Tier: Full
- Generates PEP 723 compatible Python code.
- Includes automatic dependency detection.
- Injects the latest 10 project facts for context-aware logic.
Usage: ./cli forge tool <name> <prompt>

TECHNICAL DEEP-DIVE:
The 'tool' command is the 'Production Factory' of CLIDE.
1. Intelligence: Sends the user prompt to 'gemini-2.0-flash'.
2. Templating: Applies the 'mcp_generator.get_python_mcp_template'.
3. Facts: Fetches top 10 facts using 'clide.brain.memory.get_extracted_facts'.
4. Verification: Triggers 'forge test' automatically before indexing.
5. Result: A functional, indexed MCP server ready for use in the Gemini CLI.
Primary Directory: swarm/commands/mcp_servers/.

[EXPANSION PENDING]

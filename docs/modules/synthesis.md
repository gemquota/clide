# Module: Synthesis Engines

## 1. Template Generator (`template_generator.py`)
### Purpose
Converts a raw task into a "High-Detail" system prompt.
### Flow
1. Receives task metadata.
2. Prompts Gemini to "engineer" a persona.
3. Outputs a multi-paragraph prompt with Persona, Context, Rules, and Response Style.

## 2. MCP Generator (`mcp_generator.py`)
### Purpose
Generates executable Python FastMCP servers.
### Template Logic
Injects raw shell/python logic into a FastAPI-based MCP boilerplate. This allows the tool to be called as a "function" by the LLM in future turns.

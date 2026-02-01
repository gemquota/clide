# Registry: Vector Engine

## Data Structure (`vector_registry.json`)
A JSON-based flat-file database.
### Schema
```json
{
  "id": "string",
  "metadata": {
    "type": "toml | mcp",
    "desc": "string",
    "path": "optional string"
  },
  "embedding": [0.1, 0.2, "..."] 
}
```

## Logic
- **Similarity**: Uses Cosine Similarity to find relevant assets.
- **Embedding Generation**: Currently uses a prompt-based "semantic distillation" via Gemini CLI to generate vector representations.

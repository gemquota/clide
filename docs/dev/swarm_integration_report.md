# Swarm V2 Integration Report

## 1. Executive Summary

This report details the findings from investigating `swarm/new`, which contains a "Granular Plugin Architecture" (referenced as Archon V3). The new system represents a significant evolution in agentic capability, offering a standardized, modular library of 99+ Agents and 107+ Skills across 60+ domains.

**Conclusion:** Integrating this architecture into `clide` is **highly plausible** and recommended. It would transform `clide` from a CLI assistant into a comprehensive orchestration engine for professional software engineering tasks.

## 2. Architecture Analysis: Swarm V2

The `swarm/new` directory implements a "Granular Plugin Architecture" designed for composability and token efficiency.

### Core Components
1.  **Plugins**: Logical groupings of capabilities (e.g., `kubernetes-operations`, `python-development`).
2.  **Agents (Personas)**: defined in Markdown with YAML frontmatter.
    -   *Role*: High-level reasoning and planning (e.g., `backend-architect`, `security-auditor`).
    -   *Format*: System prompts + Model preference (Opus/Sonnet/Haiku).
3.  **Skills (Knowledge)**: Modular procedural knowledge.
    -   *Structure*: Follows Anthropic's "Agent Skills Specification".
    -   *Progressive Disclosure*: 
        -   Tier 1: Metadata (Always accessible via index).
        -   Tier 2: Instructions (Loaded on activation).
        -   Tier 3: Resources (Loaded on demand).
4.  **Commands**: Specific tool definitions (Markdown/YAML) similar to `clide`'s TOML but more descriptive.

### Key Directory Structure
```
swarm/new/plugins/
├── <domain>/
│   ├── agents/    # <agent-name>.md
│   ├── skills/    # <skill-name>/SKILL.md
│   └── commands/  # <command-name>.md
```

## 3. Comparison with Clide

| Feature | Clide (Current) | Swarm V2 (Target) |
| :--- | :--- | :--- |
| **Definition** | TOML files (`commands/*.toml`) | Markdown + YAML Frontmatter |
| **Scope** | Simple shell commands + minimal context | Complex Personas + Deep Domain Knowledge |
| **Discovery** | Exact match / Simple fuzzy | Semantic Search (Vector) |
| **Context** | Single-shot context | Progressive Disclosure (Token Efficient) |
| **Orchestration**| Single command execution | Multi-agent workflows (e.g., Architect -> Dev -> QA) |

## 4. Integration Strategy

### Phase 1: Ingestion & Indexing
Leverage `clide`'s existing `vector_registry.py` to index the new assets.
- **Action**: Create a scanner `clide_src/swarm_ingestor.py` that parses `swarm/new/plugins`.
- **Logic**: Extract `name`, `description`, and `keywords` from YAML frontmatter of Agents and Skills and insert them into `vector_registry.json`.

### Phase 2: Runtime Adaptation
Update `clide`'s core loop (`clide_cli.py` / `extractor.py`) to support the new asset types.
- **Skill Activation**: When a user intent matches a Skill (via Vector Search), "mount" the skill's instructions into the active context.
- **Agent Hotswapping**: When a user intent matches an Agent, switch the system prompt to the Agent's persona (using `hotswapper.py` logic).

### Phase 3: Command Bridging
Write an adapter to execute Swarm commands using `clide`'s shell execution capabilities. Swarm commands in Markdown often contain code blocks; `clide` already has `shell_ingestor.py` which can be adapted to parse and run these.

## 5. Benefits & ROI

- **Immediate Expertise**: Instantly gain 60+ domain experts (K8s, Python, Security, etc.).
- **Token Efficiency**: The "Progressive Disclosure" model ensures we only load instructions for the specific task at hand, saving tokens and reducing noise.
- **Standardization**: Adopting the Markdown/YAML standard makes it easier for humans to write and edit skills compared to raw JSON/TOML.

## 6. Challenges

- **Context Window Management**: Managing multiple active skills could overflow context. Needs a "Garbage Collection" mechanism to unload unused skills (Context Eviction).
- **Model routing**: Swarm V2 specifies models (Opus, Sonnet). Clide currently runs on a single model configuration. We may need to ignore model preferences or implement a router if the API supports it.

## 7. Recommendation

Proceed with **Phase 1 (Ingestion)** immediately to make these assets discoverable. Follow with **Phase 2 (Runtime)** to allow manual activation of these agents.

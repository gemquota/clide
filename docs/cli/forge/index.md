# CLIDE // FORGE DOMAIN

## Tier: Basic
DETAILED USAGE
- './cli forge tool scan_logs "Find error patterns"' builds a complete MCP file.
- './cli forge test <id>' executes 'pytest' within the tool's package directory.
- './cli forge design "Database wrapper"' generates a technical blueprint without code.

## Tier: More
DETAILED USAGE
- './cli forge tool scan_logs "Find error patterns"' builds a complete MCP file.
- './cli forge test <id>' executes 'pytest' within the tool's package directory.
- './cli forge design "Database wrapper"' generates a technical blueprint without code.

TECHNICAL ARCHITECTURE: FORGE
====================================

1. THE SYNTHESIS PIPELINE (master.py)
-------------------------------------
Manufacturing follows a strictly gated sequence:
[INTENT] -> [BLUEPRINT] -> [ASSET] -> [TEST] -> [VERIFY] -> [DEPLOY]

2. CODE GENERATION (asset.py)
-----------------------------
Generates PEP 723 compatible Python scripts.
- Dependencies: Automatically detected and added to the script header.
- Framework: Standardizes on 'fastmcp' for maximum Gemini CLI compatibility.
- Context Injection: Injects the latest 10 facts from Domain [02] into the tool logic.

3. VERIFICATION & SAFETY
------------------------
- Verification: deployment is blocked if 'pytest' returns non-zero.
- Security: 'audit.py' scans for 'os.system', 'eval', and other dangerous calls.
- Manual Gate: All automated creations require manual review via 'manual' domain.

4. EVOLUTION (refine.py)
------------------------
Assets are treated as living artifacts.
- Logic Refinement: Re-prompts the LLM with the current code + user fix instruction.
- Documentation: Re-generates README.md and docstrings to match updated logic.
- Benchmarking: Measures tool latency and token consumption in a simulated run.

## Tier: Full
DETAILED USAGE
- './cli forge tool scan_logs "Find error patterns"' builds a complete MCP file.
- './cli forge test <id>' executes 'pytest' within the tool's package directory.
- './cli forge design "Database wrapper"' generates a technical blueprint without code.

TECHNICAL ARCHITECTURE: FORGE
====================================

1. THE SYNTHESIS PIPELINE (master.py)
-------------------------------------
Manufacturing follows a strictly gated sequence:
[INTENT] -> [BLUEPRINT] -> [ASSET] -> [TEST] -> [VERIFY] -> [DEPLOY]

2. CODE GENERATION (asset.py)
-----------------------------
Generates PEP 723 compatible Python scripts.
- Dependencies: Automatically detected and added to the script header.
- Framework: Standardizes on 'fastmcp' for maximum Gemini CLI compatibility.
- Context Injection: Injects the latest 10 facts from Domain [02] into the tool logic.

3. VERIFICATION & SAFETY
------------------------
- Verification: deployment is blocked if 'pytest' returns non-zero.
- Security: 'audit.py' scans for 'os.system', 'eval', and other dangerous calls.
- Manual Gate: All automated creations require manual review via 'manual' domain.

4. EVOLUTION (refine.py)
------------------------
Assets are treated as living artifacts.
- Logic Refinement: Re-prompts the LLM with the current code + user fix instruction.
- Documentation: Re-generates README.md and docstrings to match updated logic.
- Benchmarking: Measures tool latency and token consumption in a simulated run.

[EXPANSION PENDING]

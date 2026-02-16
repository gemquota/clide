import os
import time
import json
from clide.kernel import storage as db_manager
from clide.kernel.settings import load_config

def handle_analysis(analysis, msg, embedding):
    original_input = msg['message']
    category = analysis.get('category', 'NICHE')
    reasoning = analysis.get('reasoning', 'No reasoning provided.')
    
    # Ongoing Review Feedback
    print(f"  [Result] Category: {category}")
    print(f"  [Reason] {reasoning}")

    if category == "MATCH":
        cmd_name = analysis.get('command_name')
        if cmd_name:
            print(f"  [Action] Auto-activating Hotspot: {cmd_name}")
            from clide.tools.plugin import hotswap_skill, hotswap_agent
            if cmd_name.startswith("skill:"):
                hotswap_skill(cmd_name)
            elif cmd_name.startswith("agent:"):
                hotswap_agent(cmd_name)

    elif category in ["FACT", "DISCOVERY", "LESSON", "TODO"]:
        content = analysis.get('content', original_input)
        importance = analysis.get('importance', 5)
        db_manager.save_knowledge(
            category, content, original_input, importance, 
            msg.get("sessionId"), msg.get("messageId"), reasoning
        )
    
    elif category == "NEW_COMMAND":
        cmd_name = analysis.get('command_name')
        cmd_desc = analysis.get('suggested_description')
        print(f"\n>>> DETECTED POTENTIAL AGENTIC ASSET <<<")
        print(f"Name: {cmd_name} | Desc: {cmd_desc}")
        # Manual ingestion required
        db_manager.save_knowledge(
            "PROPOSAL", f"New Command: {cmd_name} - {cmd_desc}", 
            original_input, 6, msg.get("sessionId"), msg.get("messageId")
        )

    elif category == "TOOL_INTENT":
        from clide.gen.master import SynthesisOrchestrator
        orchestrator = SynthesisOrchestrator()
        result = orchestrator.process_intent(analysis)
        if result.get("status") == "success":
            print(f"\n[🔥 Forge] Successfully synthesized MCP tool: {analysis.get('tool_name')}")
        else:
            print(f"\n[!] Forge failure: {result.get('message')}")

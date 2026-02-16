import os
import shutil
import json
import yaml

class SimulationWorkspace:
    def __init__(self, workspace_id, base_dir="/data/data/com.termux/files/home/.gemini/tmp/sims"):
        self.workspace_id = workspace_id
        self.base_dir = base_dir
        self.path = os.path.join(base_dir, workspace_id)

    def create(self):
        """Creates the isolated workspace directory."""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        return self.path

    def delete(self):
        """Deletes the isolated workspace directory."""
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

    def scaffold(self):
        """Scaffolds a minimal project structure."""
        if not os.path.exists(self.path):
            self.create()
        
        os.makedirs(os.path.join(self.path, "src"), exist_ok=True)
        os.makedirs(os.path.join(self.path, "docs"), exist_ok=True)
        
        readme_path = os.path.join(self.path, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, "w") as f:
                f.write(f"# Simulation: {self.workspace_id}\n\nThis is an automated simulation workspace.")

class Scenario:
    def __init__(self, name, goal, agents, constraints=None, timeout=300, initial_state=None, success_criteria=None):
        self.name = name
        self.goal = goal
        self.agents = agents
        self.constraints = constraints or []
        self.timeout = timeout
        self.initial_state = initial_state or {}
        self.success_criteria = success_criteria or []

    @classmethod
    def from_dict(cls, data):
        required_fields = ["name", "goal", "agents"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        return cls(
            name=data["name"],
            goal=data["goal"],
            agents=data["agents"],
            constraints=data.get("constraints"),
            timeout=data.get("timeout", 300),
            initial_state=data.get("initial_state"),
            success_criteria=data.get("success_criteria")
        )

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def from_yaml(cls, yaml_str):
        data = yaml.safe_load(yaml_str)
        return cls.from_dict(data)

class Orchestrator:
    def __init__(self, scenario, workspace_base_dir="/data/data/com.termux/files/home/.gemini/tmp/sims"):
        self.scenario = scenario
        self.workspace = SimulationWorkspace(scenario.name.lower().replace(" ", "_"), workspace_base_dir)
        self.active = False
        self.current_agent = None
        self.turns = 0
        self.status = None

    def start(self):
        """Starts the simulation by preparing workspace and publishing initial goal."""
        self.workspace.create()
        self.workspace.scaffold()
        self.active = True
        self.turns = 0
        
        # Publish initial goal to the message bus
        from swarm.core.state_manager import publish_message
        publish_message(
            sender="orchestrator",
            topic="goal",
            payload_json={
                "goal": self.scenario.goal,
                "constraints": self.scenario.constraints,
                "initial_state": self.scenario.initial_state
            }
        )
        return f"Simulation '{self.scenario.name}' started in {self.workspace.path}"

    def step(self):
        """Processes the next step in the simulation."""
        if not self.active:
            return "Simulation not active."
        
        from swarm.core.state_manager import get_messages, mark_message_read
        
        self.turns += 1
        messages = get_messages(status='UNREAD')
        
        if not messages:
            return "Waiting for messages..."
        
        results = []
        for msg in messages:
            sender = msg['sender']
            topic = msg['topic']
            payload = json.loads(msg['payload']) if msg['payload'] else {}
            
            results.append(f"Processing message from {sender} on topic {topic}")
            
            # Handle handoffs
            if topic == "handoff":
                next_agent = payload.get("next_agent")
                if next_agent:
                    self.current_agent = next_agent
                    results.append(f"Handoff detected: Active agent is now {self.current_agent}")
            
            # Handle status
            if topic == "status":
                status = payload.get("status")
                if status in ["success", "failure"]:
                    self.status = status
                    results.append(f"Status update: {status}")
                    if status == "failure":
                        self.trigger_hotswap(payload.get("error"))
            
            # Mark as read
            mark_message_read(msg['id'])
            
        return "\n".join(results)

    def trigger_hotswap(self, error_msg):
        """Triggers a TOOL_INTENT to fix a simulation failure."""
        if not error_msg:
            return
            
        from swarm.core.state_manager import publish_message
        # Heuristic to find a potential tool name in the error message
        import re
        tool_match = re.search(r"'(.*?)'", error_msg)
        tool_name = tool_match.group(1) if tool_match else "unknown_fix"
        
        publish_message(
            sender="orchestrator",
            topic="TOOL_INTENT",
            payload_json={
                "tool_name": f"fix_{tool_name}",
                "description": f"Fix for failure: {error_msg}",
                "logic_code": "# Auto-generated fix placeholder\nprint('Fixing deficiency...')"
            }
        )

    def check_success(self):
        """Checks if the scenario success criteria are met."""
        if not self.scenario.success_criteria:
            return False
            
        for criterion in self.scenario.success_criteria:
            if criterion.startswith("file_exists:"):
                file_path = criterion.split(":", 1)[1].strip()
                full_path = os.path.join(self.workspace.path, file_path)
                if not os.path.exists(full_path):
                    return False
        return True

    def run(self, max_turns=20):
        """Runs the simulation loop until completion, success, or timeout."""
        self.start()
        import time
        
        for turn in range(max_turns):
            # 1. Check for success criteria first
            if self.check_success():
                self.status = "success"
                self.active = False
                return "success"
                
            # 2. Process messages
            self.step()
            
            # 3. Check for explicit success/failure messages
            if self.status in ["success", "failure"]:
                self.active = False
                return self.status
            
            time.sleep(0.1)
            
        self.active = False
        return "timeout"

    def stop(self):
        self.active = False
        return "Simulation stopped."

class CollaborationAnalyzer:
    def __init__(self):
        pass

    def _get_all_messages(self):
        from swarm.core.state_manager import get_messages
        # We want all messages, so we check both UNREAD and READ
        unread = get_messages(status='UNREAD')
        read = get_messages(status='READ')
        # Sort by ID to maintain sequence
        all_msgs = sorted(unread + read, key=lambda x: x['id'])
        return all_msgs

    def generate_summary(self):
        messages = self._get_all_messages()
        summary = {
            "total_messages": len(messages),
            "agents_involved": set(),
            "message_counts": {}
        }
        for msg in messages:
            sender = msg['sender']
            summary["agents_involved"].add(sender)
            summary["message_counts"][sender] = summary["message_counts"].get(sender, 0) + 1
        return summary

    def trace_intent(self):
        messages = self._get_all_messages()
        path = []
        last_agent = None
        for msg in messages:
            sender = msg['sender']
            if sender != last_agent:
                path.append(sender)
                last_agent = sender
        return path

    def generate_report(self):
        summary = self.generate_summary()
        path = self.trace_intent()
        path_str = " -> ".join(path)
        
        report = [
            "# Collaboration Report",
            f"Total Messages: {summary['total_messages']}",
            f"Agents Involved: {', '.join(sorted(summary['agents_involved']))}",
            "## Message Counts",
        ]
        for agent, count in summary['message_counts'].items():
            report.append(f"- {agent}: {count}")
        
        report.append("\n## Path of Intent")
        report.append(path_str)
        
        return "\n".join(report)


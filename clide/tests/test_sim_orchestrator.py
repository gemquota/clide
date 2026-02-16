import unittest
import os
import json
import shutil
from clide.sim_runner import Scenario, Orchestrator
from swarm.core.state_manager import publish_message, get_db, DB_PATH

class TestSimOrchestrator(unittest.TestCase):
    def setUp(self):
        # Clear message bus
        with get_db(DB_PATH) as conn:
            conn.execute("DELETE FROM message_bus")
        
        self.test_tmp = "/data/data/com.termux/files/home/.gemini/tmp/test_sims_orch"
        if not os.path.exists(self.test_tmp):
            os.makedirs(self.test_tmp)
            
        self.scenario_data = {
            "name": "Orchestration Test",
            "goal": "Test agent handoff",
            "agents": ["scout", "coder"]
        }
        self.scenario = Scenario.from_dict(self.scenario_data)
        self.orch = Orchestrator(self.scenario, workspace_base_dir=self.test_tmp)

    def tearDown(self):
        if os.path.exists(self.test_tmp):
            shutil.rmtree(self.test_tmp)

    def test_start_publishes_goal(self):
        self.orch.start()
        from swarm.core.state_manager import get_messages
        msgs = get_messages(topic="goal")
        self.assertEqual(len(msgs), 1)
        payload = json.loads(msgs[0]['payload'])
        self.assertEqual(payload['goal'], self.scenario.goal)

    def test_handoff_updates_current_agent(self):
        self.orch.start()
        # Mock a message from 'scout' to handoff to 'coder'
        publish_message(sender="scout", topic="handoff", payload_json={"next_agent": "coder"})
        
        # Run step
        result = self.orch.step()
        self.assertIn("Active agent is now coder", result)
        self.assertEqual(self.orch.current_agent, "coder")

    def test_multiple_messages_in_one_step(self):
        self.orch.start()
        publish_message(sender="agent1", topic="update", payload_json={"status": "working"})
        publish_message(sender="agent1", topic="handoff", payload_json={"next_agent": "agent2"})
        
        result = self.orch.step()
        self.assertIn("Processing message from agent1 on topic update", result)
        self.assertIn("Active agent is now agent2", result)

    def test_check_success_file_exists(self):
        self.scenario.success_criteria = ["file_exists: src/main.py"]
        self.orch.start()
        self.assertFalse(self.orch.check_success())
        
        # Create the file
        os.makedirs(os.path.join(self.orch.workspace.path, "src"), exist_ok=True)
        with open(os.path.join(self.orch.workspace.path, "src/main.py"), "w") as f:
            f.write("print('hello')")
            
        self.assertTrue(self.orch.check_success())

    def test_run_until_success(self):
        self.scenario.success_criteria = ["file_exists: done.txt"]
        self.orch.start()
        
        # In a real scenario, an agent would create this. Here we mock it after a short delay.
        # But run() is blocking. So we might need a separate thread if we wanted to mock "during" run.
        # Alternatively, we can test that run() returns success if the file is already there or 
        # if we mock the status message.
        
        publish_message(sender="agent", topic="status", payload_json={"status": "success"})
        status = self.orch.run(max_turns=2)
        self.assertEqual(status, "success")

if __name__ == "__main__":
    unittest.main()

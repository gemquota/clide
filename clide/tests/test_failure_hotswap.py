import unittest
import os
import json
import shutil
from clide.sim_runner import Scenario, Orchestrator
from swarm.core.state_manager import publish_message, get_db, DB_PATH

class TestFailureHotswap(unittest.TestCase):
    def setUp(self):
        with get_db(DB_PATH) as conn:
            conn.execute("DELETE FROM message_bus")
            conn.execute("DELETE FROM synthesis_events")
        
        self.test_tmp = "/data/data/com.termux/files/home/.gemini/tmp/test_sims_hotswap"
        if not os.path.exists(self.test_tmp):
            os.makedirs(self.test_tmp)

    def tearDown(self):
        if os.path.exists(self.test_tmp):
            shutil.rmtree(self.test_tmp)

    def test_failure_triggers_hotswap_event(self):
        # 1. Setup a scenario that will fail
        scenario = Scenario("Failing Sim", "Do something impossible", ["agent1"])
        orch = Orchestrator(scenario, workspace_base_dir=self.test_tmp)
        
        # 2. Mock a failure message
        publish_message("agent1", "status", {"status": "failure", "error": "Missing 'impossible_tool'"})
        
        # 3. Run Orchestrator
        status = orch.run(max_turns=2)
        self.assertEqual(status, "failure")
        
        # 4. Check if a TOOL_INTENT message was published or a hotswap was triggered
        from swarm.core.state_manager import get_messages
        hotswap_msgs = get_messages(topic="TOOL_INTENT")
        self.assertGreaterEqual(len(hotswap_msgs), 1)
        
        payload = json.loads(hotswap_msgs[0]["payload"])
        self.assertIn("impossible_tool", payload["tool_name"])

if __name__ == "__main__":
    unittest.main()

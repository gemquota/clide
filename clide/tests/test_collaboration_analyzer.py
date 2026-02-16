import unittest
import os
import json
from clide.sim_runner import CollaborationAnalyzer
from swarm.core.state_manager import publish_message, get_db, DB_PATH

class TestCollaborationAnalyzer(unittest.TestCase):
    def setUp(self):
        with get_db(DB_PATH) as conn:
            conn.execute("DELETE FROM message_bus")
            
        # Mock a simulation flow
        publish_message("orchestrator", "goal", {"goal": "build x"})
        publish_message("scout", "update", {"found": "evidence"})
        publish_message("scout", "handoff", {"next_agent": "coder"})
        publish_message("coder", "update", {"status": "coding"})
        publish_message("coder", "status", {"status": "success"})
        
        self.analyzer = CollaborationAnalyzer()

    def test_summary_generation(self):
        summary = self.analyzer.generate_summary()
        self.assertEqual(summary["total_messages"], 5)
        self.assertEqual(summary["agents_involved"], {"orchestrator", "scout", "coder"})
        self.assertEqual(summary["message_counts"]["scout"], 2)

    def test_path_of_intent(self):
        path = self.analyzer.trace_intent()
        # Path should be the sequence of agents: orchestrator -> scout -> coder
        self.assertEqual(path, ["orchestrator", "scout", "coder"])

    def test_report_formatting(self):
        report = self.analyzer.generate_report()
        self.assertIn("Collaboration Report", report)
        self.assertIn("## Path of Intent", report)
        self.assertIn("orchestrator -> scout -> coder", report)

if __name__ == "__main__":
    unittest.main()

import unittest
import json
import os
from clide.sim_runner import Scenario

class TestScenarioParser(unittest.TestCase):
    def test_parse_valid_json_scenario(self):
        scenario_data = {
            "name": "Test Scenario",
            "goal": "Build a hello world app",
            "agents": ["coder", "reviewer"],
            "constraints": ["No external libraries"],
            "timeout": 300,
            "initial_state": {
                "files": {
                    "src/main.py": "print('hello')"
                }
            },
            "success_criteria": ["file_exists: src/main.py"]
        }
        
        scenario = Scenario.from_json(json.dumps(scenario_data))
        self.assertEqual(scenario.name, "Test Scenario")
        self.assertEqual(scenario.goal, "Build a hello world app")
        self.assertIn("coder", scenario.agents)
        self.assertEqual(scenario.initial_state["files"]["src/main.py"], "print('hello')")
        self.assertIn("file_exists: src/main.py", scenario.success_criteria)

    def test_parse_yaml_scenario(self):
        yaml_content = """
name: YAML Scenario
goal: Test YAML parsing
agents:
  - scout
  - coder
constraints:
  - fast execution
initial_state:
  files:
    config.json: '{"debug": true}'
success_criteria:
  - "output_contains: SUCCESS"
"""
        scenario = Scenario.from_yaml(yaml_content)
        self.assertEqual(scenario.name, "YAML Scenario")
        self.assertEqual(scenario.goal, "Test YAML parsing")
        self.assertIn("scout", scenario.agents)
        self.assertEqual(scenario.initial_state["files"]["config.json"], '{"debug": true}')
        self.assertIn("output_contains: SUCCESS", scenario.success_criteria)

    def test_parse_invalid_scenario(self):
        # Missing required field 'goal'
        invalid_data = {"name": "Bad Scenario"}
        with self.assertRaises(ValueError):
            Scenario.from_json(json.dumps(invalid_data))

if __name__ == "__main__":
    unittest.main()

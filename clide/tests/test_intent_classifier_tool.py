import unittest
import os
import sys

# Ensure project root is in path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

class TestIntentClassifierTool(unittest.TestCase):
    def test_tool_intent_classification(self):
        from clide.brain.reason import classify_intent
        existing_commands = {}
        message = "Build a tool to calculate the area of a circle."
        
        # This might fail if the model is not set up correctly or API key is missing.
        # But we'll try it if the environment is ready.
        if not os.environ.get("GEMINI_API_KEY"):
            self.skipTest("GEMINI_API_KEY not set")
            
        result = classify_intent(message, existing_commands)
        
        self.assertEqual(result['category'], 'TOOL_INTENT')
        self.assertIn('tool_name', result)
        self.assertIn('logic_code', result)

if __name__ == '__main__':
    unittest.main()
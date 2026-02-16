import unittest
from intent_classifier import classify_intent

class TestIntentClassifierTool(unittest.TestCase):
    def test_tool_intent_classification(self):
        existing_commands = {}
        message = "Build a tool to calculate the area of a circle."
        
        # This is expected to return TOOL_INTENT after implementation
        result = classify_intent(message, existing_commands)
        
        self.assertEqual(result['category'], 'TOOL_INTENT')
        self.assertIn('tool_name', result)
        self.assertIn('logic_code', result)

if __name__ == '__main__':
    unittest.main()

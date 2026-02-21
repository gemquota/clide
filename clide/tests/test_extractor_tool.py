import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Ensure project root is in path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

class TestExtractorTool(unittest.TestCase):
    @patch('clide.forge.master.SynthesisOrchestrator.process_intent')
    def test_handle_tool_intent(self, mock_process):
        from clide.kernel.engine import handle_analysis
        
        analysis = {
            "category": "TOOL_INTENT",
            "tool_name": "test_tool",
            "logic_code": "print('hello')",
            "reasoning": "User asked for it"
        }
        msg = {"message": "Build test_tool", "sessionId": "123", "messageId": 1}
        embedding = [0.1, 0.2]
        
        mock_process.return_value = {"status": "success", "path": "/mock/path"}
        
        # We need to mock print as it might output to terminal
        with patch('builtins.print'):
            handle_analysis(analysis, msg, embedding)
        
        mock_process.assert_called_once_with(analysis)

if __name__ == '__main__':
    unittest.main()
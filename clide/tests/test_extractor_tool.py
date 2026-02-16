import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Ensure clide is in path
sys.path.append(os.path.join(os.getcwd(), 'clide'))

class TestExtractorTool(unittest.TestCase):
    @patch('synthesis_orchestrator.SynthesisOrchestrator.process_intent')
    def test_handle_tool_intent(self, mock_process):
        from extractor import handle_analysis
        
        analysis = {
            "category": "TOOL_INTENT",
            "tool_name": "test_tool",
            "logic_code": "print('hello')",
            "reasoning": "User asked for it"
        }
        msg = {"message": "Build test_tool", "sessionId": "123", "messageId": 1}
        embedding = [0.1, 0.2]
        
        mock_process.return_value = {"status": "success", "path": "/mock/path"}
        
        # We need to mock save_enriched_log as it writes to file
        with patch('extractor.save_enriched_log'):
            handle_analysis(analysis, msg, embedding)
        
        mock_process.assert_called_once_with(analysis)

if __name__ == '__main__':
    unittest.main()

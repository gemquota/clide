import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Ensure project root is in path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

class TestSynthesisOrchestrator(unittest.TestCase):
    @patch('clide.forge.master.mcp_generator.get_python_mcp_template')
    @patch('clide.forge.master.mcp_generator.save_mcp_server')
    @patch('clide.forge.master.mcp_generator.verify_and_deploy')
    @patch('clide.forge.master.vector_registry.add_to_registry')
    def test_orchestrate_synthesis(self, mock_index, mock_verify, mock_save, mock_template):
        from clide.forge.master import SynthesisOrchestrator
        
        orchestrator = SynthesisOrchestrator()
        
        # Mock template, save, and verify
        mock_template.return_value = "mock code"
        mock_save.return_value = "/path/to/mock_server.py"
        mock_verify.return_value = True
        
        intent_data = {
            "tool_name": "test_tool",
            "description": "A tool for testing",
            "logic_code": "print('hello')"
        }
        
        result = orchestrator.process_intent(intent_data)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['path'], "/path/to/mock_server.py")
        
        mock_template.assert_called_once()
        mock_save.assert_called_once()
        mock_verify.assert_called_once()
        mock_index.assert_called_once()

if __name__ == '__main__':
    unittest.main()
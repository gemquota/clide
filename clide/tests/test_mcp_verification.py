import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import shutil

# Ensure clide is in path
sys.path.append(os.path.join(os.getcwd(), 'clide'))

class TestMCPVerification(unittest.TestCase):
    def setUp(self):
        self.test_dir = "/data/data/com.termux/files/home/openclaw/meta/swarm/commands/mcp_servers/test_verify_tool"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('subprocess.run')
    def test_verify_and_deploy_success(self, mock_run):
        from mcp_generator import verify_and_deploy
        
        # Mock subprocess to return success (0)
        mock_run.return_value = MagicMock(returncode=0)
        
        # Create dummy directory and files to simulate a generated tool
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, "test_verify_tool.py"), "w") as f:
            f.write("def test_pass(): assert True")
            
        result = verify_and_deploy("test_verify_tool", self.test_dir)
        
        self.assertTrue(result)
        # Check if it was "deployed" (in this context, we just check if the logic processed it)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_verify_and_deploy_failure(self, mock_run):
        from mcp_generator import verify_and_deploy
        
        # Mock subprocess to return failure (1)
        mock_run.return_value = MagicMock(returncode=1)
        
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, "test_verify_tool.py"), "w") as f:
            f.write("def test_fail(): assert False")
            
        result = verify_and_deploy("test_verify_tool", self.test_dir)
        
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

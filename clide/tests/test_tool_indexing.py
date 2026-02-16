import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import json

# Ensure clide is in path
sys.path.append(os.path.join(os.getcwd(), 'clide'))

class TestToolIndexing(unittest.TestCase):
    @patch('vector_registry.get_embedding')
    def test_add_tool_to_registry(self, mock_emb):
        import vector_registry
        mock_emb.return_value = [0.1] * 32
        
        asset_id = "mcp:test_tool"
        metadata = {"type": "mcp", "desc": "A test tool"}
        text = "test tool description"
        
        vector_registry.add_to_registry(asset_id, metadata, text)
        
        # Verify it was added to the JSON file
        with open(vector_registry.VECTOR_DB_PATH, "r") as f:
            registry = json.load(f)
            
        found = False
        for item in registry:
            if item['id'] == asset_id:
                self.assertEqual(item['metadata']['desc'], "A test tool")
                found = True
                break
        self.assertTrue(found)

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import json

# Ensure project root is in path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

class TestToolIndexing(unittest.TestCase):
    @patch('clide.brain.memory.get_embedding')
    def test_add_tool_to_registry(self, mock_emb):
        from clide.brain import memory as vector_registry
        mock_emb.return_value = [0.1] * 768 # Standard dimension for gemini-embedding-001
        
        asset_id = "mcp:test_tool_indexing"
        metadata = {"type": "mcp", "desc": "A test tool for indexing"}
        text = "test tool description"
        
        vector_registry.add_to_registry(asset_id, metadata, text)
        
        # Verify it was added to the JSON file
        with open(vector_registry.VECTOR_DB_PATH, "r") as f:
            registry = json.load(f)
            
        found = False
        for item in registry:
            if item['id'] == asset_id:
                self.assertEqual(item['metadata']['desc'], "A test tool for indexing")
                found = True
                break
        self.assertTrue(found)

if __name__ == '__main__':
    unittest.main()
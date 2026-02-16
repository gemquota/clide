import unittest
import json
from state_manager import query_project_knowledge, MEMORY_DB_PATH, get_db

class TestMCPKnowledge(unittest.TestCase):
    def setUp(self):
        with get_db(MEMORY_DB_PATH) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, category TEXT, content TEXT, importance INTEGER)")
            conn.execute("DELETE FROM knowledge")
            conn.execute("INSERT INTO knowledge (category, content, importance) VALUES (?, ?, ?)", 
                         ('FACT', 'The system is autonomous', 10))
    
    def test_query_tool_returns_json(self):
        result_json = query_project_knowledge(text="autonomous")
        result = json.loads(result_json)
        self.assertIsInstance(result, list)
        self.assertTrue(any("autonomous" in item['content'].lower() for item in result))

if __name__ == '__main__':
    unittest.main()

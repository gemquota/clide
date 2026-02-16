import unittest
from state_manager import get_project_status, MEMORY_DB_PATH, get_db

class TestProjectStatusIntegration(unittest.TestCase):
    def setUp(self):
        with get_db(MEMORY_DB_PATH) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, category TEXT, content TEXT, importance INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
            conn.execute("DELETE FROM knowledge")
            conn.execute("INSERT INTO knowledge (category, content, importance) VALUES (?, ?, ?)", 
                         ('FACT', 'The Forge is active.', 10))

    def test_status_includes_knowledge(self):
        status = get_project_status()
        self.assertIn("Recent Knowledge:", status)
        self.assertIn("The Forge is active.", status)

if __name__ == '__main__':
    unittest.main()

import sqlite3
import os
import unittest
from swarm.core.state_manager import MEMORY_DB_PATH, KnowledgeProvider

class TestKnowledgeProvider(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Add mock data for testing to the real test db path (or a temp one)
        # For this task, we use the MEMORY_DB_PATH defined in state_manager
        with sqlite3.connect(MEMORY_DB_PATH) as conn:
            conn.execute("DELETE FROM knowledge WHERE content IN ('The sky is blue.', 'Always check for nulls.')")
            conn.execute("INSERT INTO knowledge (category, content, importance) VALUES (?, ?, ?)", 
                         ('FACT', 'The sky is blue.', 8))
            conn.execute("INSERT INTO knowledge (category, content, importance) VALUES (?, ?, ?)", 
                         ('LESSON', 'Always check for nulls.', 9))
            conn.commit()

    def test_knowledge_provider_exists(self):
        self.assertIsNotNone(KnowledgeProvider, "KnowledgeProvider class should be implemented in state_manager.py")

    def test_query_all(self):
        kp = KnowledgeProvider()
        results = kp.query_knowledge()
        # We expect at least our 2 mock items
        contents = [r['content'] for r in results]
        self.assertIn('The sky is blue.', contents)
        self.assertIn('Always check for nulls.', contents)
        
    def test_filter_by_category(self):
        kp = KnowledgeProvider()
        results = kp.query_knowledge(category='LESSON')
        for r in results:
            self.assertEqual(r['category'], 'LESSON')
        contents = [r['content'] for r in results]
        self.assertIn('Always check for nulls.', contents)

    def test_filter_by_importance(self):
        kp = KnowledgeProvider()
        results = kp.query_knowledge(min_importance=9)
        for r in results:
            self.assertGreaterEqual(r['importance'], 9)
        contents = [r['content'] for r in results]
        self.assertIn('Always check for nulls.', contents)
        self.assertNotIn('The sky is blue.', contents)

if __name__ == '__main__':
    unittest.main()
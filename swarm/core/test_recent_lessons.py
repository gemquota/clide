import unittest
import json
from state_manager import get_recent_lessons, MEMORY_DB_PATH, get_db

class TestRecentLessons(unittest.TestCase):
    def setUp(self):
        with get_db(MEMORY_DB_PATH) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, category TEXT, content TEXT, importance INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
            conn.execute("DELETE FROM knowledge")
            conn.execute("INSERT INTO knowledge (category, content, importance) VALUES (?, ?, ?)", 
                         ('LESSON', 'Lesson 1', 5))
            conn.execute("INSERT INTO knowledge (category, content, importance) VALUES (?, ?, ?)", 
                         ('LESSON', 'Lesson 2', 5))
            conn.execute("INSERT INTO knowledge (category, content, importance) VALUES (?, ?, ?)", 
                         ('FACT', 'Not a lesson', 5))
    
    def test_get_lessons_returns_only_lessons(self):
        result_json = get_recent_lessons(limit=10)
        result = json.loads(result_json)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        for item in result:
            self.assertEqual(item['category'], 'LESSON')

if __name__ == '__main__':
    unittest.main()

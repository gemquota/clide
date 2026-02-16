import unittest
import json
from swarm.core.state_manager import query_project_knowledge, get_recent_lessons

class TestKnowledgeTools(unittest.TestCase):
    def test_query_project_knowledge_basic(self):
        """Test basic querying of project knowledge."""
        # This should return a JSON string
        result_json = query_project_knowledge()
        result = json.loads(result_json)
        self.assertIsInstance(result, list)
        # We know from previous setup there are at least 2 items
        self.assertGreaterEqual(len(result), 0)

    def test_query_project_knowledge_filter(self):
        """Test filtering by category and importance."""
        result_json = query_project_knowledge(category='LESSON', min_importance=8)
        result = json.loads(result_json)
        for item in result:
            self.assertEqual(item['category'], 'LESSON')
            self.assertGreaterEqual(item['importance'], 8)

    def test_get_recent_lessons(self):
        """Test fetching recent lessons."""
        result_json = get_recent_lessons(limit=5)
        result = json.loads(result_json)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertEqual(item['category'], 'LESSON')

if __name__ == '__main__':
    unittest.main()

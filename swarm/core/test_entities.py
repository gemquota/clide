import unittest
from swarm.core.state_manager import init_entity, get_db, DB_PATH

class TestEntities(unittest.TestCase):
    def setUp(self):
        with get_db(DB_PATH) as conn:
            conn.execute("DELETE FROM entities")

    def test_init_feature(self):
        result = init_entity("new feature", "FEATURE")
        self.assertIn("Successfully initialized FEATURE", result)

    def test_init_bug(self):
        result = init_entity("new bug", "BUG")
        self.assertIn("Successfully initialized BUG", result)

if __name__ == "__main__":
    unittest.main()

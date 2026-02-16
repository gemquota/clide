import sqlite3
import os
import unittest
from state_manager import get_db, DB_PATH

class TestDBConcurrency(unittest.TestCase):
    def test_wal_mode_enabled(self):
        """Verify that both databases are in WAL mode."""
        # Check state.db
        from state_manager import DB_PATH, MEMORY_DB_PATH
        with get_db(DB_PATH) as conn:
            cursor = conn.execute("PRAGMA journal_mode;")
            mode = cursor.fetchone()[0]
            self.assertEqual(mode.upper(), 'WAL', "state.db should be in WAL mode")
        
        # Check memory.db
        with get_db(MEMORY_DB_PATH) as conn:
            cursor = conn.execute("PRAGMA journal_mode;")
            mode = cursor.fetchone()[0]
            self.assertEqual(mode.upper(), 'WAL', "memory.db should be in WAL mode")

if __name__ == '__main__':
    unittest.main()

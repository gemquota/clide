import sqlite3
import os
import unittest
import threading
import time
from state_manager import get_db, DB_PATH, MEMORY_DB_PATH

class TestStateSyncPhase1(unittest.TestCase):
    def setUp(self):
        # Ensure clean state if possible, or just use existing
        pass

    def test_wal_mode_active(self):
        """Ensure WAL mode is active on both databases."""
        for path in [DB_PATH, MEMORY_DB_PATH]:
            with get_db(path) as conn:
                mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
                self.assertEqual(mode.upper(), 'WAL')

    def test_concurrent_access(self):
        """Test that we can read from memory.db while writing to state.db."""
        errors = []

        def writer():
            try:
                with get_db(DB_PATH) as conn:
                    conn.execute("INSERT INTO entities (name, type) VALUES (?, ?)", ("Test Concurrent", "FEATURE"))
                    # Hold the connection for a bit
                    time.sleep(0.1)
                    conn.commit()
            except Exception as e:
                errors.append(f"Writer error: {e}")

        def reader():
            try:
                with get_db(MEMORY_DB_PATH) as conn:
                    # Just a simple read
                    conn.execute("SELECT count(*) FROM knowledge").fetchone()
            except Exception as e:
                errors.append(f"Reader error: {e}")

        t1 = threading.Thread(target=writer)
        t2 = threading.Thread(target=reader)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        self.assertEqual(len(errors), 0, f"Concurrency errors occurred: {errors}")

if __name__ == '__main__':
    unittest.main()

import unittest
import sqlite3
import os
from state_manager import get_db, DB_PATH, record_synthesis

class TestSynthesisRecording(unittest.TestCase):
    def test_record_synthesis_event(self):
        tool_name = "test_record_tool"
        status = "success"
        details = "Forged successfully"
        
        result = record_synthesis(tool_name, status, details)
        self.assertIn("Successfully recorded", result)
        
        # Verify in DB
        with get_db(DB_PATH) as conn:
            row = conn.execute("SELECT * FROM synthesis_events WHERE tool_name = ?", (tool_name,)).fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row['status'], status)

if __name__ == '__main__':
    unittest.main()

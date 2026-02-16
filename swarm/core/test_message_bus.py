import unittest
import sqlite3
import os
import json
from swarm.core.state_manager import get_db, DB_PATH, publish_message, get_messages

class TestMessageBus(unittest.TestCase):
    def setUp(self):
        with get_db(DB_PATH) as conn:
            conn.execute("DELETE FROM message_bus")

    def test_publish_and_retrieve_message(self):
        topic = "test_topic"
        sender = "agent_a"
        payload = {"task": "do something"}
        
        result = publish_message(sender, topic, payload)
        self.assertIn("Successfully published", result)
        
        messages = get_messages(topic=topic)
        self.assertGreaterEqual(len(messages), 1)
        self.assertEqual(messages[0]['sender'], sender)
        self.assertEqual(json.loads(messages[0]['payload']), payload)

    def test_topic_filtering(self):
        publish_message("agent_b", "topic_1", "msg 1")
        publish_message("agent_c", "topic_2", "msg 2")
        
        msgs_1 = get_messages(topic="topic_1")
        self.assertEqual(len(msgs_1), 1)
        self.assertEqual(msgs_1[0]['sender'], "agent_b")
        
        msgs_2 = get_messages(topic="topic_2")
        self.assertEqual(len(msgs_2), 1)
        self.assertEqual(msgs_2[0]['sender'], "agent_c")

    def test_mark_as_read(self):
        from swarm.core.state_manager import mark_message_read
        publish_message("agent_d", "topic_3", "msg 3")
        msgs = get_messages(topic="topic_3")
        msg_id = msgs[0]['id']
        
        mark_message_read(msg_id)
        
        msgs_after = get_messages(topic="topic_3", status='UNREAD')
        # Check that it's no longer in UNREAD
        self.assertFalse(any(m['id'] == msg_id for m in msgs_after))
        
        msgs_read = get_messages(topic="topic_3", status='READ')
        self.assertTrue(any(m['id'] == msg_id for m in msgs_read))

if __name__ == "__main__":
    unittest.main()

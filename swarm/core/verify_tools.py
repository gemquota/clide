import json
import os
from swarm.core.state_manager import query_project_knowledge, get_recent_lessons, MEMORY_DB_PATH, get_db

def verify():
    print("--- Phase 2 Manual Verification ---")
    
    # 1. Ensure test data exists in memory.db
    with get_db(MEMORY_DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, category TEXT, content TEXT, importance INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        conn.execute("INSERT INTO knowledge (category, content, importance) VALUES (?, ?, ?)", 
                     ('FACT', 'Verification: The Forge is active.', 10))
        conn.execute("INSERT INTO knowledge (category, content, importance) VALUES (?, ?, ?)", 
                     ('LESSON', 'Verification: Always verify your syncs.', 8))
    
    # 2. Test query_project_knowledge
    print("\nTesting 'query_project_knowledge' (Searching for 'Forge'):")
    search_result = query_project_knowledge(text="Forge")
    print(search_result)
    
    # 3. Test get_recent_lessons
    print("\nTesting 'get_recent_lessons':")
    lessons_result = get_recent_lessons(limit=1)
    print(lessons_result)

if __name__ == "__main__":
    verify()

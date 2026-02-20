import sqlite3
import os

SRC_DB = "clide/memory.db.bak"
DST_DB = "clide/memory_recovered_final.db"

if os.path.exists(DST_DB):
    os.remove(DST_DB)

src_conn = sqlite3.connect(SRC_DB)
dst_conn = sqlite3.connect(DST_DB)

# Create schema in destination
dst_conn.executescript("""
    CREATE TABLE knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        content TEXT,
        original_msg TEXT,
        importance INTEGER DEFAULT 5,
        embedding BLOB,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        importance_score FLOAT DEFAULT 5.0, 
        last_accessed DATETIME DEFAULT '1970-01-01 00:00:00', 
        session_id TEXT, 
        message_id INTEGER, 
        tags TEXT, 
        review TEXT, 
        model_response TEXT, 
        model_thoughts TEXT, 
        command_name TEXT
    );
""")

src_cursor = src_conn.cursor()
count = 0
errors = 0

try:
    # Try to get all IDs first to iterate individually
    src_cursor.execute("SELECT id FROM knowledge")
    ids = [row[0] for row in src_cursor.fetchall()]
    print(f"Found {len(ids)} potential IDs")
    
    for row_id in ids:
        try:
            src_cursor.execute("SELECT * FROM knowledge WHERE id = ?", (row_id,))
            row = src_cursor.fetchone()
            if row:
                placeholders = ",".join(["?"] * len(row))
                # Note: We skip the first column (id) if we want autoincrement to handle it, 
                # or we include it if we want to preserve IDs.
                # Here we include it to preserve relationships.
                dst_conn.execute(f"INSERT INTO knowledge VALUES ({placeholders})", row)
                count += 1
                if count % 100 == 0:
                    print(f"Recovered {count} rows...")
        except Exception as e:
            errors += 1
            continue
except Exception as e:
    print(f"Primary fetch failed: {e}")
    # Fallback: scan by ID range if SELECT id failed
    print("Attempting brute-force ID scan...")
    for row_id in range(1, 100000): # Adjust range as needed
        try:
            src_cursor.execute("SELECT * FROM knowledge WHERE id = ?", (row_id,))
            row = src_cursor.fetchone()
            if row:
                placeholders = ",".join(["?"] * len(row))
                dst_conn.execute(f"INSERT INTO knowledge VALUES ({placeholders})", row)
                count += 1
        except:
            continue

dst_conn.commit()
src_conn.close()
dst_conn.close()

print(f"Recovery complete. Total rows: {count}, Errors: {errors}")

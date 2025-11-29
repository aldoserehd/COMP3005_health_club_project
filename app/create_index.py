from config import engine
from sqlalchemy import text

index_sql = """
CREATE INDEX IF NOT EXISTS idx_ptsession_start
ON pt_sessions(start_time);
"""

with engine.connect() as conn:
    conn.execute(text(index_sql))
    print("Index created: idx_ptsession_start")

from config import engine
from sqlalchemy import text

sql = """
CREATE OR REPLACE VIEW member_latest_metric AS
SELECT
    m.id AS member_id,
    m.full_name,
    hm.recorded_at,
    hm.weight,
    hm.heart_rate,
    hm.body_fat_percentage
FROM members m
LEFT JOIN LATERAL (
    SELECT *
    FROM health_metrics
    WHERE health_metrics.member_id = m.id
    ORDER BY recorded_at DESC
    LIMIT 1
) hm ON true;
"""

with engine.connect() as conn:
    conn.execute(text(sql))
    print("View created: member_latest_metric")

from config import engine
from sqlalchemy import text

trigger_sql = """
CREATE OR REPLACE FUNCTION prevent_overlapping_pt()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM pt_sessions
        WHERE member_id = NEW.member_id
          AND status != 'cancelled'
          AND NEW.start_time < end_time
          AND NEW.end_time > start_time
    ) THEN
        RAISE EXCEPTION 'Member already has a PT session during this time.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS prevent_overlap_trigger ON pt_sessions;

CREATE TRIGGER prevent_overlap_trigger
BEFORE INSERT ON pt_sessions
FOR EACH ROW
EXECUTE FUNCTION prevent_overlapping_pt();
"""

with engine.connect() as conn:
    conn.execute(text(trigger_sql))
    print("Trigger created: prevent_overlapping_pt")

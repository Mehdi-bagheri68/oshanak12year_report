import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def inspect_acepta():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT sent_time, subject, recipients_to, body_snippet
        FROM emails
        WHERE phase='Phase 1' AND subject LIKE '%اکسپتا%'
        ORDER BY sent_time ASC
    """)
    rows = cur.fetchall()
    print(f"Total Acepta emails: {len(rows)}")
    for stime, subj, rto, body in rows[:10]:
        print(f"[{stime[:10]}] Subj: {subj} | To: {rto[:30]}")
        print(f"   {body[:300].replace(chr(10), ' ')}...\n")
        
    conn.close()

if __name__ == '__main__':
    inspect_acepta()

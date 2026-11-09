import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def inspect_weekly_reports():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT sent_time, subject, body_snippet
        FROM emails
        WHERE subject LIKE '%گزارش کار%' OR subject LIKE '%شرح گزارش%'
        ORDER BY sent_time ASC
    """)
    for stime, subj, body in cur.fetchall():
        print("="*60)
        print(f"[{stime[:10]}] Subject: {subj}")
        print("Body:")
        print(body[:1500])
        print("\n")
        
    conn.close()

if __name__ == '__main__':
    inspect_weekly_reports()

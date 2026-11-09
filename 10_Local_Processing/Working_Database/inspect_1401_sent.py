import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def inspect():
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cur = conn.cursor()
    
    print("\n=================== SENT EMAILS IN 1401 (Phase 5) ===================")
    cur.execute("""
        SELECT sent_time, subject, recipients_to, body_snippet
        FROM emails
        WHERE phase='Phase 5 (1401)' AND folder_name='Sent Items'
        AND (subject LIKE '%دیتابیس%' OR subject LIKE '%oltp%' OR subject LIKE '%سرور%' OR subject LIKE '%dll%' OR subject LIKE '%مودیان%' OR subject LIKE '%تخفیف%' OR subject LIKE '%پوز%')
        ORDER BY sent_time ASC LIMIT 10
    """)
    for r in cur.fetchall():
        print(f"[{r[0][:10]}] Subj: {r[1]} | To: {r[2][:35]}")
        body = (r[3] or '')[:200].replace('\n', ' ')
        print(f"   {body}...\n")
        
    conn.close()

if __name__ == '__main__':
    inspect()

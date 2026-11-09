import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def inspect():
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cur = conn.cursor()
    
    for yr, ph in [('1398', 'Phase 2 (1398)'), ('1399', 'Phase 3 (1399)'), ('1400', 'Phase 4 (1400)')]:
        print(f"\n=================== SENT EMAILS SAMPLE IN {yr} ({ph}) ===================")
        cur.execute("""
            SELECT sent_time, subject, recipients_to, body_snippet
            FROM emails
            WHERE phase=? AND folder_name='Sent Items'
            ORDER BY sent_time ASC LIMIT 5
        """, (ph,))
        for r in cur.fetchall():
            print(f"[{r[0][:10]}] Subj: {r[1]} | To: {r[2][:35]}")
            body = (r[3] or '')[:200].replace('\n', ' ')
            print(f"   {body}...\n")
            
    conn.close()

if __name__ == '__main__':
    inspect()

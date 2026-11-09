import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def inspect_sent():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    years = [
        ("1394", "2015-05-01", "2016-03-20"),
        ("1395", "2016-03-20", "2017-03-21"),
        ("1396", "2017-03-21", "2018-03-21"),
        ("1397", "2018-03-21", "2019-03-22"),
    ]
    
    for yr, d1, d2 in years:
        print(f"\n=================== SAMPLE SENT EMAILS IN {yr} ===================")
        cur.execute("""
            SELECT id, sent_time, subject, recipients_to, recipients_cc, body_snippet
            FROM emails
            WHERE folder_name='Sent Items' AND sent_time >= ? AND sent_time < ?
            ORDER BY sent_time ASC
            LIMIT 15
        """, (d1, d2))
        for row in cur.fetchall():
            mid, stime, subj, rto, rcc, body = row
            snippet = body[:200].replace('\n', ' ').replace('\r', '') if body else ""
            print(f"[{stime[:10]}] To: {rto[:30]} | Subj: {subj}")
            print(f"   Snippet: {snippet}...\n")
            
    conn.close()

if __name__ == '__main__':
    inspect_sent()

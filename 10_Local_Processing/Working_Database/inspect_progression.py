import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def inspect_progression():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\n--- KEY EMAILS FROM 1395 (2016-2017) ---")
    cur.execute("""
        SELECT sent_time, subject, recipients_to, body_snippet
        FROM emails
        WHERE folder_name='Sent Items' AND sent_time >= '2016-03-21' AND sent_time < '2017-03-21'
        AND (subject LIKE '%رشت%' OR subject LIKE '%گیلان%' OR subject LIKE '%شمال%' OR subject LIKE '%انبار%' OR subject LIKE '%گزارش%' OR subject LIKE '%پروژه%' OR subject LIKE '%سرور%')
        ORDER BY sent_time ASC
        LIMIT 10
    """)
    for stime, subj, rto, body in cur.fetchall():
        print(f"[{stime[:10]}] Subj: {subj} | To: {rto[:30]}")
        print(f"   {body[:250].replace(chr(10), ' ')}...\n")
        
    print("\n--- KEY EMAILS FROM 1396 (2017-2018) ---")
    cur.execute("""
        SELECT sent_time, subject, recipients_to, body_snippet
        FROM emails
        WHERE folder_name='Sent Items' AND sent_time >= '2017-03-21' AND sent_time < '2018-03-21'
        AND (subject LIKE '%منطقه%' OR subject LIKE '%شمال%' OR subject LIKE '%تجهیزات%' OR subject LIKE '%شبکه%' OR subject LIKE '%ax%' OR subject LIKE '%pos%' OR subject LIKE '%صندوق%')
        ORDER BY sent_time ASC
        LIMIT 10
    """)
    for stime, subj, rto, body in cur.fetchall():
        print(f"[{stime[:10]}] Subj: {subj} | To: {rto[:30]}")
        print(f"   {body[:250].replace(chr(10), ' ')}...\n")
        
    print("\n--- KEY EMAILS FROM 1397 (2018-2019) ---")
    cur.execute("""
        SELECT sent_time, subject, recipients_to, body_snippet
        FROM emails
        WHERE folder_name='Sent Items' AND sent_time >= '2018-03-21' AND sent_time < '2019-03-21'
        AND (subject LIKE '%منطقه%' OR subject LIKE '%مازندران%' OR subject LIKE '%گیلان%' OR subject LIKE '%اکسپتا%' OR subject LIKE '%نرم افزار%' OR subject LIKE '%انبارگردانی%' OR subject LIKE '%پوز%')
        ORDER BY sent_time ASC
        LIMIT 10
    """)
    for stime, subj, rto, body in cur.fetchall():
        print(f"[{stime[:10]}] Subj: {subj} | To: {rto[:30]}")
        print(f"   {body[:250].replace(chr(10), ' ')}...\n")
        
    conn.close()

if __name__ == '__main__':
    inspect_progression()

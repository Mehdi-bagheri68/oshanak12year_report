import sqlite3
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def inspect_signatures():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("--- EXTRACTING SIGNATURES FROM SENT EMAILS ---")
    cur.execute("""
        SELECT sent_time, body_snippet
        FROM emails
        WHERE folder_name='Sent Items' AND body_snippet LIKE '%مهدی باقری%'
        ORDER BY sent_time ASC
    """)
    rows = cur.fetchall()
    
    signatures = set()
    for stime, body in rows:
        # search for signature lines around 'مهدی باقری'
        lines = body.split('\n')
        for i, line in enumerate(lines):
            if 'مهدی باقری' in line or 'Mehdi bagheri' in line or 'Mehdi Bagheri' in line:
                # get next 3 lines
                sig = " // ".join([l.strip() for l in lines[max(0, i-1):min(len(lines), i+4)] if l.strip()])
                if len(sig) > 15 and len(sig) < 250:
                    signatures.add((stime[:7], sig))
                    
    # Sort by date
    for dt, s in sorted(signatures):
        print(f"[{dt}] {s}")
        
    conn.close()

if __name__ == '__main__':
    inspect_signatures()

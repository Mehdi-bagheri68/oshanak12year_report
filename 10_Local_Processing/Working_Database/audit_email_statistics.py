import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"
PHASE1_BACKUP_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence_phase1_backup.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("=== 1. CHECKPOINTS LOG ===")
    cur.execute("SELECT year, phase_label, inbox_count, sent_count, total_count, attachments_count, completed_at FROM checkpoints_log ORDER BY year")
    for r in cur.fetchall():
        print(f"Year {r[0]} ({r[1]}): Inbox={r[2]}, Sent={r[3]}, Total={r[4]}, Atts={r[5]}, Completed={r[6]}")
        
    print("\n=== 2. EMAILS TABLE BREAKDOWN BY PHASE ===")
    cur.execute("""
        SELECT phase, 
               count(*) as total,
               sum(CASE WHEN folder_name = 'Inbox' THEN 1 ELSE 0 END) as f_inbox,
               sum(CASE WHEN folder_name = 'Sent Items' THEN 1 ELSE 0 END) as f_sent,
               sum(CASE WHEN is_sent_by_me = 1 THEN 1 ELSE 0 END) as is_sent_true,
               sum(CASE WHEN is_sent_by_me = 0 THEN 1 ELSE 0 END) as is_sent_false,
               min(sent_time),
               max(sent_time)
        FROM emails
        GROUP BY phase
        ORDER BY phase
    """)
    for r in cur.fetchall():
        print(f"Phase: {r[0]} | Total: {r[1]} | Fldr Inbox: {r[2]} | Fldr Sent: {r[3]} | SentByMe: {r[4]} | SentByOther: {r[5]} | Min: {r[6]} | Max: {r[7]}")
        
    print("\n=== 3. PHASE 1 DISCREPANCY INVESTIGATION ===")
    # Check Phase 1 in current DB
    cur.execute("""
        SELECT count(*),
               sum(CASE WHEN folder_name = 'Inbox' THEN 1 ELSE 0 END),
               sum(CASE WHEN folder_name = 'Sent Items' THEN 1 ELSE 0 END),
               sum(CASE WHEN is_sent_by_me = 1 THEN 1 ELSE 0 END),
               sum(CASE WHEN is_sent_by_me = 0 THEN 1 ELSE 0 END)
        FROM emails
        WHERE phase = 'Phase 1 (1394-1397)'
    """)
    r_curr = cur.fetchone()
    print(f"Current DB Phase 1: Total={r_curr[0]}, Fldr Inbox={r_curr[1]}, Fldr Sent={r_curr[2]}, is_sent_by_me=1={r_curr[3]}, is_sent_by_me=0={r_curr[4]}")
    
    # Check Phase 1 in backup DB
    if os.path.exists(PHASE1_BACKUP_PATH):
        conn_p1 = sqlite3.connect(PHASE1_BACKUP_PATH)
        cur_p1 = conn_p1.cursor()
        cur_p1.execute("""
            SELECT count(*),
                   sum(CASE WHEN folder_name = 'Inbox' THEN 1 ELSE 0 END),
                   sum(CASE WHEN folder_name = 'Sent Items' THEN 1 ELSE 0 END),
                   sum(CASE WHEN is_sent_by_me = 1 THEN 1 ELSE 0 END),
                   sum(CASE WHEN is_sent_by_me = 0 THEN 1 ELSE 0 END)
            FROM emails
        """)
        r_p1 = cur_p1.fetchone()
        print(f"Backup DB Phase 1: Total={r_p1[0]}, Fldr Inbox={r_p1[1]}, Fldr Sent={r_p1[2]}, is_sent_by_me=1={r_p1[3]}, is_sent_by_me=0={r_p1[4]}")
        
        # Check why is_sent_by_me differs from folder_name in Phase 1
        cur_p1.execute("""
            SELECT count(*) FROM emails WHERE folder_name = 'Inbox' AND is_sent_by_me = 1
        """)
        inbox_sent_by_me = cur_p1.fetchone()[0]
        cur_p1.execute("""
            SELECT count(*) FROM emails WHERE folder_name = 'Sent Items' AND is_sent_by_me = 0
        """)
        sent_not_by_me = cur_p1.fetchone()[0]
        print(f"Phase 1 Backup details: Inbox emails sent by me: {inbox_sent_by_me}, Sent Items not sent by me: {sent_not_by_me}")
        conn_p1.close()

    print("\n=== 4. TOTAL UNIQUE EMAILS & DUPLICATES ===")
    cur.execute("SELECT count(*), count(DISTINCT entry_id) FROM emails")
    tot_cnt, dist_cnt = cur.fetchone()
    print(f"Total rows: {tot_cnt}, Distinct entry_id: {dist_cnt}")
    
    cur.execute("""
        SELECT count(*) FROM (
            SELECT subject, sent_time, count(*) as c 
            FROM emails 
            GROUP BY subject, sent_time 
            HAVING c > 1
        )
    """)
    dup_subj_time = cur.fetchone()[0]
    print(f"Potential subject + sent_time duplicate groups: {dup_subj_time}")

    print("\n=== 5. OVERALL STORE DISTRIBUTION ===")
    cur.execute("SELECT store_name, count(*) FROM emails GROUP BY store_name")
    for r in cur.fetchall():
        print(f"Store: {r[0]} | Count: {r[1]}")

    print("\n=== 6. DATE RANGE & 1405 MAXIMUM DATE ===")
    cur.execute("SELECT min(sent_time), max(sent_time) FROM emails")
    min_all, max_all = cur.fetchone()
    print(f"Overall Date Range: Min={min_all} | Max={max_all}")
    
    cur.execute("SELECT min(sent_time), max(sent_time), min(received_time), max(received_time) FROM emails WHERE phase LIKE '%1405%'")
    min_1405_s, max_1405_s, min_1405_r, max_1405_r = cur.fetchone()
    print(f"Phase 9 (1405) Range: Sent Min={min_1405_s}, Sent Max={max_1405_s} | Received Min={min_1405_r}, Received Max={max_1405_r}")

    conn.close()

if __name__ == '__main__':
    main()

import sqlite3
import os
import sys
import json
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def analyze_all_years():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Check what phases we have in emails table
    cur.execute("SELECT DISTINCT phase FROM emails ORDER BY phase")
    phases = [r[0] for r in cur.fetchall()]
    print(f"Phases present in database: {phases}")
    
    summary = {}
    
    for phase in phases:
        cur.execute("SELECT count(*) FROM emails WHERE phase=?", (phase,))
        total = cur.fetchone()[0]
        
        cur.execute("SELECT count(*) FROM emails WHERE phase=? AND is_sent_by_me=1", (phase,))
        sent = cur.fetchone()[0]
        
        inbox = total - sent
        
        cur.execute("""
            SELECT count(a.id) FROM attachments a
            JOIN emails e ON a.email_entry_id = e.entry_id
            WHERE e.phase=?
        """, (phase,))
        atts = cur.fetchone()[0]
        
        # Top senders
        cur.execute("""
            SELECT sender_name, count(*) as cnt 
            FROM emails 
            WHERE phase=? AND is_sent_by_me=0 AND sender_name != ''
            GROUP BY sender_name 
            ORDER BY cnt DESC LIMIT 10
        """, (phase,))
        top_senders = cur.fetchall()
        
        # Top recipients when sent by me
        cur.execute("""
            SELECT recipients_to, count(*) as cnt 
            FROM emails 
            WHERE phase=? AND is_sent_by_me=1 AND recipients_to != ''
            GROUP BY recipients_to 
            ORDER BY cnt DESC LIMIT 10
        """, (phase,))
        top_recipients = cur.fetchall()
        
        # Sample interesting subjects
        cur.execute("""
            SELECT subject, sent_time, sender_name, recipients_to, is_sent_by_me
            FROM emails
            WHERE phase=? AND (
                subject LIKE '%AX%' OR subject LIKE '%پوز%' OR subject LIKE '%صندوق%' OR
                subject LIKE '%SQL%' OR subject LIKE '%مودیان%' OR subject LIKE '%مغایرت%' OR
                subject LIKE '%جلسه%' OR subject LIKE '%پروژه%' OR subject LIKE '%انبار%' OR
                subject LIKE '%گزارش%' OR subject LIKE '%سامانه%' OR subject LIKE '%سرور%' OR
                subject LIKE '%Power%' OR subject LIKE '%BI%' OR subject LIKE '%ارتقا%'
            )
            ORDER BY sent_time ASC
            LIMIT 30
        """, (phase,))
        sample_key_emails = cur.fetchall()
        
        summary[phase] = {
            "total": total,
            "sent": sent,
            "inbox": inbox,
            "attachments": atts,
            "top_senders": top_senders,
            "top_recipients": top_recipients,
            "sample_key_emails": sample_key_emails
        }
        print(f"Analyzed {phase}: Total={total}, Sent={sent}, Inbox={inbox}, Atts={atts}")
        
    conn.close()
    return summary

if __name__ == '__main__':
    res = analyze_all_years()

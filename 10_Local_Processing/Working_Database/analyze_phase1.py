import sqlite3
import sys
import os
import json
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def analyze():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("=" * 60)
    print("PHASE 1 (1394-1397) FORENSIC ANALYSIS SUMMARY")
    print("=" * 60)
    
    # 1. Total Counts
    cur.execute("SELECT COUNT(*) FROM emails WHERE phase='Phase 1'")
    total_emails = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM emails WHERE phase='Phase 1' AND folder_name='Inbox'")
    inbox_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM emails WHERE phase='Phase 1' AND folder_name='Sent Items'")
    sent_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM emails WHERE phase='Phase 1' AND is_sent_by_me=1")
    my_sent = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM attachments")
    total_atts = cur.fetchone()[0]
    
    print(f"Total Emails: {total_emails}")
    print(f"  - Inbox: {inbox_count}")
    print(f"  - Sent Items: {sent_count} (Sent by Mehdi Bagheri: {my_sent})")
    print(f"Total Attachments: {total_atts}")
    
    # 2. Date breakdown by Solar year
    print("\n--- Distribution by Solar Year ---")
    # 1394: 2015-03-21 to 2016-03-19
    # 1395: 2016-03-20 to 2017-03-20
    # 1396: 2017-03-21 to 2018-03-20
    # 1397: 2018-03-21 to 2019-03-20
    year_queries = [
        ("1394 (2015/05 - 2016/03)", "2015-05-01", "2016-03-20"),
        ("1395 (2016/03 - 2017/03)", "2016-03-20", "2017-03-21"),
        ("1396 (2017/03 - 2018/03)", "2017-03-21", "2018-03-21"),
        ("1397 (2018/03 - 2019/03)", "2018-03-21", "2019-03-22"),
    ]
    for label, d_start, d_end in year_queries:
        cur.execute("""
            SELECT COUNT(*), SUM(CASE WHEN folder_name='Sent Items' THEN 1 ELSE 0 END)
            FROM emails 
            WHERE phase='Phase 1' AND received_time >= ? AND received_time < ?
        """, (d_start, d_end))
        tot, sent = cur.fetchone()
        tot = tot or 0
        sent = sent or 0
        print(f"  Year {label}: Total={tot}, Sent by user={sent}")
        
    # 3. Key Interlocutors (Senders / Recipients)
    print("\n--- Top 15 Senders to Mehdi Bagheri ---")
    cur.execute("""
        SELECT sender_name, sender_email, COUNT(*) as c
        FROM emails
        WHERE phase='Phase 1' AND folder_name='Inbox'
        GROUP BY sender_email
        ORDER BY c DESC
        LIMIT 15
    """)
    for row in cur.fetchall():
        print(f"  {row[2]} emails: {row[0]} <{row[1]}>")
        
    # 4. Top Conversation Topics
    print("\n--- Top 20 Conversation Topics (Clusters) ---")
    cur.execute("""
        SELECT conversation_topic, COUNT(*) as c, MIN(received_time), MAX(received_time)
        FROM emails
        WHERE phase='Phase 1' AND conversation_topic != ''
        GROUP BY conversation_topic
        ORDER BY c DESC
        LIMIT 25
    """)
    for row in cur.fetchall():
        print(f"  [{row[1]} msgs] ({str(row[2])[:10]} to {str(row[3])[:10]}): {row[0]}")
        
    # 5. Attachment Analysis
    print("\n--- Attachment Types ---")
    cur.execute("""
        SELECT extension, COUNT(*) as c
        FROM attachments
        GROUP BY extension
        ORDER BY c DESC
        LIMIT 10
    """)
    for row in cur.fetchall():
        print(f"  {row[0] or '[no ext]'}: {row[1]} files")
        
    # 6. Search for Key Themes / Keywords
    print("\n--- Keyword Presence (Email Counts) ---")
    keywords = [
        "فروشگاه", "pos", "پوز", "شبکه", "اینترنت", "روتر", "سوییچ", "میکروتیک",
        "تلفن", "ویپ", "voip", "سرور", "اکتیو دایرکتوری", "domain", "آنتی ویروس",
        "پشتیبان", "backup", "ax", "dynamics", "داینامیک", "صندوق", "بارکدخوان",
        "لیبل پرینتر", "اسکنر", "چک لیست", "افتتاح", "نصب", "قطعی", "ارتقا", "مجوز"
    ]
    for kw in keywords:
        cur.execute("""
            SELECT COUNT(*) FROM emails
            WHERE phase='Phase 1' AND (subject LIKE ? OR body_snippet LIKE ?)
        """, (f"%{kw}%", f"%{kw}%"))
        print(f"  Keyword '{kw}': {cur.fetchone()[0]} occurrences")
        
    conn.close()

if __name__ == '__main__':
    analyze()

import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def inspect_year(phase_label):
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    cur = conn.cursor()
    
    print(f"\n=================== {phase_label} ===================")
    cur.execute("SELECT COUNT(*), SUM(is_sent_by_me) FROM emails WHERE phase=?", (phase_label,))
    tot, sent = cur.fetchone()
    print(f"Total: {tot}, Sent by user: {sent}")
    
    print("\nTop 15 Conversation Topics:")
    cur.execute("""
        SELECT conversation_topic, COUNT(*) as c, MIN(received_time), MAX(received_time)
        FROM emails
        WHERE phase=? AND conversation_topic != ''
        GROUP BY conversation_topic
        ORDER BY c DESC LIMIT 15
    """, (phase_label,))
    for r in cur.fetchall():
        print(f"   [{r[1]} msgs] ({str(r[2])[:10]} to {str(r[3])[:10]}): {r[0]}")
        
    print("\nTop 10 Senders:")
    cur.execute("""
        SELECT sender_name, sender_email, COUNT(*) as c
        FROM emails
        WHERE phase=? AND folder_name='Inbox'
        GROUP BY sender_email
        ORDER BY c DESC LIMIT 10
    """, (phase_label,))
    for r in cur.fetchall():
        print(f"   [{r[2]}] {r[0]} <{r[1]}>")
        
    print("\nKey Enterprise Keywords:")
    kws = ["ax", "dynamics", "pos", "صندوق", "اکسپتا", "storeconnect", "cdx", "sql", "دیتابیس", "پرتال", "انبارگردانی", "مغایرت", "فروشگاه"]
    for kw in kws:
        cur.execute("""
            SELECT COUNT(*) FROM emails
            WHERE phase=? AND (subject LIKE ? OR body_snippet LIKE ?)
        """, (phase_label, f"%{kw}%", f"%{kw}%"))
        print(f"   Keyword '{kw}': {cur.fetchone()[0]}")
        
    conn.close()

if __name__ == '__main__':
    for ph in ["Phase 2 (1398)", "Phase 3 (1399)"]:
        inspect_year(ph)

import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def search_exact(title, kw):
    print(f"\n=======================================================")
    print(f"=== {title}: kw='{kw}' ===")
    print(f"=======================================================")
    cur.execute("""
        SELECT phase, sent_time, folder_name, is_sent_by_me, sender_name, recipients_to, subject, body_snippet
        FROM emails
        WHERE subject LIKE ? OR body_snippet LIKE ?
        ORDER BY sent_time ASC
        LIMIT 25
    """, (f"%{kw}%", f"%{kw}%"))
    rows = cur.fetchall()
    print(f"Matches: {len(rows)}")
    for idx, r in enumerate(rows, 1):
        phase, s_time, fldr, is_sent, sndr, recip, subj, snip = r
        clean_snip = (snip or "").replace("\r", " ").replace("\n", " ")[:160]
        print(f"[{idx}] {phase} | {str(s_time)[:10]} | {sndr} -> {recip}")
        print(f"    Subj: {subj}")
        print(f"    Snip: {clean_snip}...")

search_exact("ZABETPOUR (ضابط پور)", "ضابط پور")
search_exact("PEDRAM SIMA (سیما)", "پدرام سیما")
search_exact("RECRUITMENT MAZANDARAN/GILAN", "جذب نیرو")
search_exact("INTERVIEW (مصاحبه)", "مصاحبه")
search_exact("TRAINING CASHIERS (آموزش صندوقداران)", "آموزش")
search_exact("MANUAL/DOCUMENTATION (فایل آموزشی)", "فایل آموزشی")

conn.close()

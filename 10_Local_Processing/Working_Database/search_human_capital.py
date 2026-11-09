import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def search_keywords(category_name, keywords, limit=50):
    print(f"\n=======================================================")
    print(f"=== {category_name} (Top {limit} Matches) ===")
    print(f"=======================================================")
    
    where_clauses = []
    params = []
    for kw in keywords:
        where_clauses.append("(subject LIKE ? OR body_snippet LIKE ?)")
        params.extend([f"%{kw}%", f"%{kw}%"])
        
    query = f"""
        SELECT phase, sent_time, folder_name, is_sent_by_me, sender_name, recipients_to, subject, attachment_names, body_snippet
        FROM emails
        WHERE {" OR ".join(where_clauses)}
        ORDER BY sent_time ASC
        LIMIT {limit}
    """
    cur.execute(query, params)
    rows = cur.fetchall()
    print(f"Total matching rows returned: {len(rows)}")
    
    for idx, r in enumerate(rows, 1):
        phase, s_time, fldr, is_sent, sndr, recip, subj, atts, snip = r
        clean_snip = (snip or "").replace("\r", " ").replace("\n", " ")[:160]
        sent_tag = "[SENT BY ME]" if is_sent else "[RECEIVED]"
        print(f"\n[{idx}] {phase} | {str(s_time)[:10]} | {sent_tag} | {sndr} -> {recip}")
        print(f"    Subject: {subj}")
        if atts:
            print(f"    Atts: {atts[:100]}")
        print(f"    Snippet: {clean_snip}...")

# 1. Recruitment & Staffing
search_keywords("1. RECRUITMENT & HIRING (استخدام، مصاحبه، رزومه، جذب نیرو)", [
    "استخدام", "مصاحبه", "رزومه", "جذب نیرو", "نیروی جدید", "پرسنلی", "حکم کارگزینی", "همکار جدید", "ضابط پور", "سیما", "شکیبایی"
], limit=35)

# 2. Employee & User Training
search_keywords("2. TRAINING & EDUCATION (آموزش، راهنما، داکیومنت، صندوقدار، کارگاه)", [
    "آموزش", "کلاس آموزشی", "فایل آموزشی", "راهنمای کاربری", "دستورالعمل", "آموزش صندوق", "آموزش سیستم", "آموزش پرسنل", "آموزش هندهلد", "راهنمای نرم افزار"
], limit=35)

# 3. Knowledge Management & SOPs
search_keywords("3. KNOWLEDGE MANAGEMENT & SOPs (چک لیست، پرتال، شیرپوینت، Knowledge)", [
    "چک لیست", "SOP", "شیرپوینت", "فرآیند", "روند کار", "مستند", "Knowledge", "داکیومنت", "صورتجلسه", "پرتال"
], limit=30)

# 4. Performance & Shift Management
search_keywords("4. PERFORMANCE & TEAM MANAGEMENT (شیفت، اضافه کار، مرخصی، انبارگردانی)", [
    "شیفت", "اضافه کار", "مرخصی", "انبارگردانی", "جدول کشیک", "تقسیم کار", "ارزیابی", "تیکت", "سامانه کلیک"
], limit=30)

# 5. Stakeholders & Cross-Functional Coordination
search_keywords("5. STAKEHOLDER COORDINATION (حاجی، پوربابا، کیانی، صافیان، موسوی، پرستار)", [
    "حاجی", "پوربابا", "کیانی", "صافیان", "جواد موسوی", "مرمر پرستار", "جلسه هماهنگی", "معاونت اجرایی"
], limit=35)

conn.close()

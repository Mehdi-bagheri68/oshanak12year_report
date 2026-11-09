import win32com.client
import sqlite3
import os
import sys
import datetime
import time

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"D:\Oshanak_Career_Intelligence_1394_1405"
DB_PATH = os.path.join(BASE_DIR, r"10_Local_Processing\Working_Database\career_intelligence.db")
LOG_PATH = os.path.join(BASE_DIR, r"00_Project_Control\Processing_Log.md")

CHECKPOINTS = [
    ("1398", "Phase 2 (1398)", "03/21/2019 00:00", "03/19/2020 23:59", [6]),
    ("1399", "Phase 3 (1399)", "03/20/2020 00:00", "03/20/2021 23:59", [6]),
    ("1400", "Phase 4 (1400)", "03/21/2021 00:00", "03/20/2022 23:59", [6]),
    ("1401", "Phase 5 (1401)", "03/21/2022 00:00", "03/20/2023 23:59", [6]),
    ("1402", "Phase 6 (1402)", "03/21/2023 00:00", "03/19/2024 23:59", [6]),
    ("1403", "Phase 7 (1403)", "03/20/2024 00:00", "03/20/2025 23:59", [6]),
    ("1404", "Phase 8 (1404)", "03/21/2025 00:00", "03/20/2026 23:59", [6, 7]),
    ("1405", "Phase 9 (1405)", "03/21/2026 00:00", "12/31/2026 23:59", [7, 4]),
]

def log_msg(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"- **{ts}:** {msg}"
    print(formatted, flush=True)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except:
        pass

def clean_str(val):
    if val is None:
        return ""
    return str(val).strip()

def init_tables(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS checkpoints_log (
        year TEXT PRIMARY KEY,
        phase_label TEXT,
        inbox_count INTEGER,
        sent_count INTEGER,
        total_count INTEGER,
        attachments_count INTEGER,
        completed_at TEXT
    )
    """)
    conn.commit()

def extract_year(ol, ns, conn, year, phase_label, start_dt, end_dt, store_indices):
    cur = conn.cursor()
    cur.execute("SELECT total_count FROM checkpoints_log WHERE year=?", (year,))
    row = cur.fetchone()
    if row and row[0] > 0:
        log_msg(f"Year {year} already extracted ({row[0]} items). Skipping extraction.")
        return row[0]
        
    log_msg(f"Beginning extraction for Year {year} ({phase_label})...")
    total_year_saved = 0
    total_year_atts = 0
    inbox_saved = 0
    sent_saved = 0
    
    for s_idx in store_indices:
        s = ns.Stores.Item(s_idx)
        s_name = s.DisplayName
        root = s.GetRootFolder()
        
        for fldr_name in ["Inbox", "Sent Items"]:
            try:
                folder = root.Folders[fldr_name]
            except:
                continue
                
            date_field = "[ReceivedTime]" if fldr_name == "Inbox" else "[SentOn]"
            filter_str = f"{date_field} >= '{start_dt}' AND {date_field} <= '{end_dt}'"
            
            try:
                items = folder.Items.Restrict(filter_str)
            except Exception as e:
                log_msg(f"Error restricting {s_name} -> {fldr_name}: {e}")
                continue
                
            count_fldr = items.Count
            if count_fldr == 0:
                continue
                
            log_msg(f"   Extracting {s_name} -> {fldr_name} ({count_fldr} items)...")
            
            batch = []
            att_batch = []
            item = items.GetFirst()
            processed = 0
            
            while item:
                processed += 1
                try:
                    entry_id = clean_str(getattr(item, "EntryID", None))
                    if not entry_id:
                        item = items.GetNext()
                        continue
                        
                    subject = clean_str(getattr(item, "Subject", ""))
                    conv_topic = clean_str(getattr(item, "ConversationTopic", subject))
                    conv_id = clean_str(getattr(item, "ConversationID", ""))
                    
                    sender_name = clean_str(getattr(item, "SenderName", ""))
                    sender_email = clean_str(getattr(item, "SenderEmailAddress", ""))
                    recipients_to = clean_str(getattr(item, "To", ""))
                    recipients_cc = clean_str(getattr(item, "CC", ""))
                    
                    sent_on = getattr(item, "SentOn", None)
                    received_time = getattr(item, "ReceivedTime", None)
                    sent_time_str = sent_on.isoformat() if sent_on else ""
                    recv_time_str = received_time.isoformat() if received_time else ""
                    
                    importance = getattr(item, "Importance", 1)
                    
                    atts = getattr(item, "Attachments", None)
                    att_count = atts.Count if atts else 0
                    has_attachments = 1 if att_count > 0 else 0
                    att_names = []
                    
                    if has_attachments:
                        for a_idx in range(1, min(att_count + 1, 25)):
                            try:
                                att_obj = atts.Item(a_idx)
                                fn = clean_str(getattr(att_obj, "FileName", f"att_{a_idx}"))
                                sz = getattr(att_obj, "Size", 0)
                                ext = os.path.splitext(fn)[1].lower()
                                att_names.append(fn)
                                att_batch.append((entry_id, fn, ext, sz, ""))
                            except:
                                pass
                                
                    att_names_str = " | ".join(att_names)
                    
                    body_snippet = ""
                    try:
                        b = getattr(item, "Body", None)
                        if b:
                            body_snippet = b[:1500].strip()
                    except:
                        pass
                        
                    is_me = 0
                    if "mbagheri" in sender_email.lower() or "باغری" in sender_name or "مهدی باقری" in sender_name:
                        is_me = 1
                    elif fldr_name == "Sent Items":
                        is_me = 1
                        
                    batch.append((
                        entry_id, s_name, fldr_name, phase_label, conv_id, conv_topic,
                        subject, sender_name, sender_email, recipients_to, recipients_cc,
                        sent_time_str, recv_time_str, importance, has_attachments,
                        att_names_str, att_count, body_snippet, is_me
                    ))
                    
                    if len(batch) >= 250:
                        cur.executemany("""
                        INSERT OR IGNORE INTO emails (
                            entry_id, store_name, folder_name, phase, conversation_id, conversation_topic,
                            subject, sender_name, sender_email, recipients_to, recipients_cc,
                            sent_time, received_time, importance, has_attachments, attachment_names,
                            attachment_count, body_snippet, is_sent_by_me
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, batch)
                        if att_batch:
                            cur.executemany("""
                            INSERT INTO attachments (email_entry_id, filename, extension, size, extracted_path)
                            VALUES (?, ?, ?, ?, ?)
                            """, att_batch)
                            total_year_atts += len(att_batch)
                            att_batch = []
                        conn.commit()
                        if fldr_name == "Inbox":
                            inbox_saved += len(batch)
                        else:
                            sent_saved += len(batch)
                        total_year_saved += len(batch)
                        batch = []
                        print(f"      [{year}] {fldr_name}: {processed}/{count_fldr} saved...", flush=True)
                except Exception as ex:
                    pass
                    
                try:
                    item = items.GetNext()
                except:
                    break
                    
            if batch:
                cur.executemany("""
                INSERT OR IGNORE INTO emails (
                    entry_id, store_name, folder_name, phase, conversation_id, conversation_topic,
                    subject, sender_name, sender_email, recipients_to, recipients_cc,
                    sent_time, received_time, importance, has_attachments, attachment_names,
                    attachment_count, body_snippet, is_sent_by_me
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, batch)
                if att_batch:
                    cur.executemany("""
                    INSERT INTO attachments (email_entry_id, filename, extension, size, extracted_path)
                    VALUES (?, ?, ?, ?, ?)
                    """, att_batch)
                    total_year_atts += len(att_batch)
                conn.commit()
                if fldr_name == "Inbox":
                    inbox_saved += len(batch)
                else:
                    sent_saved += len(batch)
                total_year_saved += len(batch)
                
    cur.execute("""
    INSERT OR REPLACE INTO checkpoints_log (year, phase_label, inbox_count, sent_count, total_count, attachments_count, completed_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (year, phase_label, inbox_saved, sent_saved, total_year_saved, total_year_atts, datetime.datetime.now().isoformat()))
    conn.commit()
    
    log_msg(f"Year {year} extraction complete: {total_year_saved} emails (Inbox: {inbox_saved}, Sent: {sent_saved}), {total_year_atts} attachments.")
    return total_year_saved

def main():
    log_msg("=== Launching Master Multi-Year Extraction Pipeline (1398-1405) ===")
    conn = sqlite3.connect(DB_PATH)
    init_tables(conn)
    
    ol = win32com.client.dynamic.Dispatch("Outlook.Application")
    ns = ol.GetNamespace("MAPI")
    
    grand_total = 0
    for cp in CHECKPOINTS:
        yr, phase, s_dt, e_dt, s_idxs = cp
        t0 = time.time()
        c = extract_year(ol, ns, conn, yr, phase, s_dt, e_dt, s_idxs)
        grand_total += c
        dur = time.time() - t0
        log_msg(f"Checkpoint [{yr}] finished in {dur:.1f}s.")
        
    conn.close()
    log_msg(f"=== Master Extraction Finished! Total 1398-1405 emails in database: {grand_total} ===")

if __name__ == '__main__':
    main()

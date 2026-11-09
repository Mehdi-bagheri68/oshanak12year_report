import win32com.client
import sqlite3
import os
import sys
import datetime

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_id TEXT UNIQUE,
        store_name TEXT,
        folder_name TEXT,
        phase TEXT,
        conversation_id TEXT,
        conversation_topic TEXT,
        subject TEXT,
        sender_name TEXT,
        sender_email TEXT,
        recipients_to TEXT,
        recipients_cc TEXT,
        sent_time TEXT,
        received_time TEXT,
        importance INTEGER,
        has_attachments INTEGER,
        attachment_names TEXT,
        attachment_count INTEGER,
        body_snippet TEXT,
        is_sent_by_me INTEGER
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attachments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email_entry_id TEXT,
        filename TEXT,
        extension TEXT,
        size INTEGER,
        extracted_path TEXT
    )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_emails_date ON emails(received_time)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_emails_sender ON emails(sender_email)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_emails_phase ON emails(phase)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_emails_topic ON emails(conversation_topic)")
    conn.commit()
    return conn

def clean_str(val):
    if val is None:
        return ""
    return str(val).strip()

def extract_folder(folder, folder_name, phase_name, conn, filter_str=None):
    cur = conn.cursor()
    items = folder.Items
    if filter_str:
        items = items.Restrict(filter_str)
    
    total = items.Count
    print(f"[*] Extracting {folder_name} (Total restricted: {total})...", flush=True)
    
    count = 0
    saved = 0
    skipped = 0
    
    # Iterate through items
    item = items.GetFirst()
    batch = []
    att_batch = []
    
    while item:
        count += 1
        try:
            # Check message class (skip non-mail items if needed, or include meeting items)
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
            
            # Attachments
            atts = getattr(item, "Attachments", None)
            att_count = atts.Count if atts else 0
            has_attachments = 1 if att_count > 0 else 0
            att_names = []
            
            if has_attachments:
                for a_idx in range(1, min(att_count + 1, 30)):
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
            
            # Body snippet
            body_snippet = ""
            try:
                body = getattr(item, "Body", None)
                if body:
                    body_snippet = body[:2000].strip()
            except:
                pass
            
            is_me = 0
            if "mbagheri" in sender_email.lower() or "باغری" in sender_name or "مهدی باقری" in sender_name:
                is_me = 1
            elif folder_name == "Sent Items":
                is_me = 1
                
            batch.append((
                entry_id,
                "mbagheri-archive-1404",
                folder_name,
                phase_name,
                conv_id,
                conv_topic,
                subject,
                sender_name,
                sender_email,
                recipients_to,
                recipients_cc,
                sent_time_str,
                recv_time_str,
                importance,
                has_attachments,
                att_names_str,
                att_count,
                body_snippet,
                is_me
            ))
            
            if len(batch) >= 200:
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
                    att_batch = []
                    
                conn.commit()
                saved += len(batch)
                batch = []
                print(f"   Processed {count}/{total} items ({saved} saved)...", flush=True)
                
        except Exception as ex:
            skipped += 1
            
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
        conn.commit()
        saved += len(batch)
        
    print(f"[+] Completed {folder_name}: {count} processed, {saved} saved, {skipped} skipped.\n", flush=True)

def main():
    print("=== Starting Phase 1 (1394-1397) Local Extraction ===", flush=True)
    conn = init_db()
    ol = win32com.client.dynamic.Dispatch("Outlook.Application")
    ns = ol.GetNamespace("MAPI")
    s = ns.Stores.Item(6) # mbagheri-archive-1404
    root = s.GetRootFolder()
    
    filter_inbox = "[ReceivedTime] >= '05/01/2015 00:00' AND [ReceivedTime] <= '03/21/2019 23:59'"
    filter_sent = "[SentOn] >= '05/01/2015 00:00' AND [SentOn] <= '03/21/2019 23:59'"
    
    inbox = root.Folders['Inbox']
    extract_folder(inbox, "Inbox", "Phase 1", conn, filter_inbox)
    
    sent = root.Folders['Sent Items']
    extract_folder(sent, "Sent Items", "Phase 1", conn, filter_sent)
    
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM emails WHERE phase='Phase 1'")
    total_emails = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM attachments")
    total_atts = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM emails WHERE phase='Phase 1' AND is_sent_by_me=1")
    my_emails = cur.fetchone()[0]
    
    print(f"=== Extraction Complete ===")
    print(f"Total Phase 1 emails in DB: {total_emails}")
    print(f"Total Phase 1 sent by me: {my_emails}")
    print(f"Total attachments recorded: {total_atts}")
    
    conn.close()

if __name__ == '__main__':
    main()

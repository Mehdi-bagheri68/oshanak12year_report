import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Let's check sender_email, sender_name in Phase 1
cur.execute("SELECT count(*) FROM emails WHERE phase='Phase 1'")
print("Phase 1 total:", cur.fetchone()[0])

cur.execute("SELECT count(*) FROM emails WHERE phase='Phase 1' AND folder_name='Inbox'")
print("Phase 1 folder=Inbox:", cur.fetchone()[0])

cur.execute("SELECT count(*) FROM emails WHERE phase='Phase 1' AND folder_name='Sent Items'")
print("Phase 1 folder=Sent Items:", cur.fetchone()[0])

# Check is_sent_by_me vs sender_email
cur.execute("SELECT count(*) FROM emails WHERE phase='Phase 1' AND sender_email LIKE '%mbagheri%'")
print("Phase 1 sender_email like mbagheri:", cur.fetchone()[0])

cur.execute("SELECT count(*) FROM emails WHERE phase='Phase 1' AND sender_name LIKE '%Bagheri%'")
print("Phase 1 sender_name like Bagheri:", cur.fetchone()[0])

# Check if 31 emails in Sent Items had blank sender or different sender
cur.execute("SELECT count(*) FROM emails WHERE phase='Phase 1' AND folder_name='Sent Items' AND (sender_email NOT LIKE '%mbagheri%' AND sender_name NOT LIKE '%Bagheri%')")
print("Phase 1 Sent Items but sender not Bagheri:", cur.fetchone()[0])

# Check sent_time vs received_time or date boundaries
cur.execute("SELECT count(*) FROM emails WHERE phase='Phase 1' AND sent_time >= '2015-05-01' AND sent_time <= '2019-03-21'")
print("Phase 1 date bounded:", cur.fetchone()[0])

# What if someone did: Total (7080) minus 2191?
# Where could 2191 come from?
# 2222 - 31 = 2191.
# What are those 31 emails?
cur.execute("SELECT count(*) FROM emails WHERE phase='Phase 1' AND folder_name='Sent Items' AND (recipients_to IS NULL OR recipients_to = '')")
print("Phase 1 Sent Items with empty recipients_to:", cur.fetchone()[0])

cur.execute("SELECT count(*) FROM emails WHERE phase='Phase 1' AND folder_name='Sent Items' AND (subject IS NULL OR subject = '' OR subject LIKE 'Automatic reply%')")
print("Phase 1 Sent Items auto reply or empty subject:", cur.fetchone()[0])

# Check distinct conversation_id or drafts/meeting requests
cur.execute("SELECT count(*) FROM emails WHERE phase='Phase 1' AND folder_name='Sent Items' AND subject LIKE '%Undeliverable%'")
print("Phase 1 Sent Items Undeliverable:", cur.fetchone()[0])

# Check if 31 emails had is_sent_by_me = 0 in some previous run or script
# Let's inspect extract_phase1.py!
conn.close()

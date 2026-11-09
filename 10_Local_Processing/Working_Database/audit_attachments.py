import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("=== ATTACHMENT FORENSIC AUDIT ===")
cur.execute("SELECT count(*) FROM attachments")
tot_att_rows = cur.fetchone()[0]
print(f"Total attachment rows in DB: {tot_att_rows}")

cur.execute("SELECT count(DISTINCT email_entry_id || '_' || filename) FROM attachments")
unique_per_email = cur.fetchone()[0]
print(f"Unique (email_entry_id + filename): {unique_per_email}")

cur.execute("SELECT count(DISTINCT filename) FROM attachments")
dist_filenames = cur.fetchone()[0]
print(f"Distinct filenames: {dist_filenames}")

cur.execute("SELECT count(DISTINCT filename || '_' || size) FROM attachments")
dist_fn_size = cur.fetchone()[0]
print(f"Distinct (filename + size): {dist_fn_size}")

# Top repeated filenames (signatures, logos, etc.)
cur.execute("""
    SELECT filename, count(*) as cnt 
    FROM attachments 
    GROUP BY filename 
    ORDER BY cnt DESC 
    LIMIT 15
""")
print("\nTop 15 repeated attachment filenames (signatures/logos/templates):")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]} occurrences")

# Check attachments per phase
cur.execute("""
    SELECT e.phase, count(a.id), count(DISTINCT a.filename || '_' || a.size)
    FROM attachments a
    JOIN emails e ON a.email_entry_id = e.entry_id
    GROUP BY e.phase
    ORDER BY e.phase
""")
print("\nAttachments per phase (Total rows vs Distinct filename+size):")
for r in cur.fetchall():
    print(f"  Phase {r[0]}: Total rows = {r[1]}, Unique (name+size) = {r[2]}")

# Check extracted_path: how many were physically extracted to disk
cur.execute("SELECT count(*) FROM attachments WHERE extracted_path IS NOT NULL AND extracted_path != ''")
extracted_cnt = cur.fetchone()[0]
print(f"\nAttachments with extracted_path recorded: {extracted_cnt}")

conn.close()

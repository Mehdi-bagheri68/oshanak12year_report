import win32com.client
import sys

sys.stdout.reconfigure(encoding='utf-8')
ol = win32com.client.dynamic.Dispatch('Outlook.Application')
ns = ol.GetNamespace('MAPI')

checkpoints = [
    ('1398', '03/21/2019 00:00', '03/19/2020 23:59', [6]),
    ('1399', '03/20/2020 00:00', '03/20/2021 23:59', [6]),
    ('1400', '03/21/2021 00:00', '03/20/2022 23:59', [6]),
    ('1401', '03/21/2022 00:00', '03/20/2023 23:59', [6]),
    ('1402', '03/21/2023 00:00', '03/19/2024 23:59', [6]),
    ('1403', '03/20/2024 00:00', '03/20/2025 23:59', [6]),
    ('1404', '03/21/2025 00:00', '03/20/2026 23:59', [6, 7]),
    ('1405', '03/21/2026 00:00', '12/31/2026 23:59', [7, 4]),
]

print("=== CHECKPOINT ITEM COUNTS (1398 - 1405) ===")
total_all = 0
for label, start_dt, end_dt, store_indices in checkpoints:
    inbox_tot = 0
    sent_tot = 0
    for s_idx in store_indices:
        s = ns.Stores.Item(s_idx)
        root = s.GetRootFolder()
        try:
            inbox = root.Folders['Inbox']
            r_inbox = inbox.Items.Restrict(f"[ReceivedTime] >= '{start_dt}' AND [ReceivedTime] <= '{end_dt}'")
            inbox_tot += r_inbox.Count
        except Exception as e:
            pass
        try:
            sent = root.Folders['Sent Items']
            r_sent = sent.Items.Restrict(f"[SentOn] >= '{start_dt}' AND [SentOn] <= '{end_dt}'")
            sent_tot += r_sent.Count
        except Exception as e:
            pass
    tot = inbox_tot + sent_tot
    total_all += tot
    print(f"Checkpoint [{label}] ({start_dt[:10]} - {end_dt[:10]}): Inbox={inbox_tot}, Sent={sent_tot}, Total={tot}")

print(f"Total across all 8 checkpoints (1398-1405): {total_all}")

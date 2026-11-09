import win32com.client
import sys

sys.stdout.reconfigure(encoding='utf-8')
ol = win32com.client.dynamic.Dispatch('Outlook.Application')
ns = ol.GetNamespace('MAPI')
s = ns.Stores.Item(6) # mbagheri-archive-1404
root = s.GetRootFolder()

# Date filter for Phase 1: 2015-05-01 to 2019-03-21
filter_inbox = "[ReceivedTime] >= '05/01/2015 00:00' AND [ReceivedTime] <= '03/21/2019 23:59'"
filter_sent = "[SentOn] >= '05/01/2015 00:00' AND [SentOn] <= '03/21/2019 23:59'"

inbox = root.Folders['Inbox']
restricted_inbox = inbox.Items.Restrict(filter_inbox)
print(f"Restricted Inbox items (1394-1397): {restricted_inbox.Count}")

sent = root.Folders['Sent Items']
restricted_sent = sent.Items.Restrict(filter_sent)
print(f"Restricted Sent items (1394-1397): {restricted_sent.Count}")

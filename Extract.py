from datetime import datetime
from Lumen_policy import lumen
from Zayo_policy import zayo


def extract_information(message, cid_dict):
    subject = message.Subject
    sender = message.SenderName
    # print(sender)
    body = message.body.splitlines()
    received_time = message.ReceivedTime
    save_email_flag = False
    my_time = []
    reason = ""
    cid = []

    # Lumen
    if sender == 'No-Reply@Lumen.com':
        reason, my_time, cid = lumen(message)
    elif sender == 'MR Zayo':
        reason, my_time, cid = zayo(message)
    # if sender == "Verizon"
    # if sender == "Arelion"

    # Format the important information
    if cid:
        print("=" * 50)
        print(f"Subject: {subject}")
        print(f"Sender: {sender}")
        print(f"Received Time: {received_time}")
        print(f"Reason for MW: {reason}\nVendor CID is {cid}\nTime is {my_time}")
        print("=" * 50)
        now = datetime.now()
        year, month, day = now.year, now.month, now.day
        filename = f"MW_info_{year}-{month}-{day}"
        with (open(filename, 'a') as w):
            for cur_cid in cid:
                all_info = f"Subject: {subject}\n"+f"Reason for MW: {reason}\nVendor CID is {cur_cid}\nTime is {my_time}\n"
                if cur_cid in cid_dict:
                    w.write(all_info)
                    w.write(f"CT CID: {cid_dict[cur_cid]}")
                    w.write("\n\n")
                    save_email_flag = True
                if cur_cid not in cid_dict:
                    w.write(all_info)
                    w.write(f"Customer's CID or not in the database. Check manually!")
                    w.write("\n\n")

    return save_email_flag

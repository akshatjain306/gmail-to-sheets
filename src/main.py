# from gmail_service import get_gmail_service
# from email_parser import parse_email
# from sheets_service import append_row
# from config import SHEET_ID

# def main():
#     gmail = get_gmail_service()

#     results = gmail.users().messages().list(
#         userId='me',
#         labelIds=['INBOX', 'UNREAD']
#     ).execute()

#     messages = results.get('messages', [])

#     if not messages:
#         print("No new unread emails.")
#         return

#     for msg in messages:
#         msg_id = msg['id']

#         message = gmail.users().messages().get(
#             userId='me', id=msg_id, format='full'
#         ).execute()

#         parsed = parse_email(message)

#         append_row(SHEET_ID, [
#             parsed['from'],
#             parsed['subject'],
#             parsed['date'],
#             parsed['content']
#         ])

#         # Mark email as read
#         gmail.users().messages().modify(
#             userId='me',
#             id=msg_id,
#             body={'removeLabelIds': ['UNREAD']}
#         ).execute()

#         print("Processed:", parsed['subject'])

# if __name__ == "__main__":
#     main()











from gmail_service import get_gmail_service
from email_parser import parse_email
from sheets_service import append_row
from config import SHEET_ID
import os

STATE_FILE = "processed_ids.txt"

def load_processed_ids():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_processed_id(msg_id):
    with open(STATE_FILE, "a") as f:
        f.write(msg_id + "\n")

def main():
    gmail = get_gmail_service()
    processed_ids = load_processed_ids()

    results = gmail.users().messages().list(
        userId='me',
        labelIds=['INBOX', 'UNREAD']
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("No new unread emails.")
        return

    for msg in messages:
        msg_id = msg['id']

        # 🔐 DUPLICATE PREVENTION
        if msg_id in processed_ids:
            continue

        message = gmail.users().messages().get(
            userId='me', id=msg_id, format='full'
        ).execute()

        parsed = parse_email(message)

        append_row(SHEET_ID, [
            parsed['from'],
            parsed['subject'],
            parsed['date'],
            parsed['content']
        ])

        gmail.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

        save_processed_id(msg_id)
        print("Processed:", parsed['subject'])

if __name__ == "__main__":
    main()

import imaplib
import email
from email.header import decode_header

IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "yanxinyu1998@gmail.com"
APP_PASSWORD = "xxxx xxxx xxxx xxxx"

imap = imaplib.IMAP4_SSL(IMAP_SERVER)
imap.login(EMAIL_ACCOUNT, APP_PASSWORD)

# 选择收件箱
imap.select("INBOX")

# 搜索最近未读邮件
status, messages = imap.search(None, "UNSEEN")
mail_ids = messages[0].split()

print(f"未读邮件数: {len(mail_ids)}")

for mail_id in mail_ids[:5]:  # 先取 5 封
    _, msg_data = imap.fetch(mail_id, "(RFC822)")
    raw_email = msg_data[0][1]

    msg = email.message_from_bytes(raw_email)

    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8", errors="ignore")

    print("主题:", subject)
    print("发件人:", msg.get("From"))
    print("-" * 40)

imap.logout()

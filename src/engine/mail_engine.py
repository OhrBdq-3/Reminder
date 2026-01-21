import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime, timedelta
from utils.helper import load_setting


class MailEngine:
    def __init__(self):
        self.cfg = self._load_setting()
        
        
    def _load_setting(self,):
        setting = load_setting()
        return {
            "imap_server":setting["mail_setting"].get("imap_server","imap.gmail.com"),
            "account":setting["mail_setting"].get("account",""),
            "password":setting["mail_setting"].get("app_password",""),
        }
        
    def _load_imap(self,):
        if self.cfg:
            try:
                self.imap = imaplib.IMAP4_SSL(self.cfg["imap_server"])
                self.imap.login(self.cfg["account"], self.cfg["password"])
                self.imap.select("INBOX")
            except TimeoutError:
                print('timeout')
        
            
    def pull_mails(self):
        self._load_setting()
        self._load_imap()
        try:
            result_list = []
            today = datetime.utcnow().date()
            tomorrow = today + timedelta(days=1)

            imap_today = today.strftime("%d-%b-%Y")
            imap_tomorrow = tomorrow.strftime("%d-%b-%Y")
            
            search_criteria = f'(SINCE "{imap_today}" BEFORE "{imap_tomorrow}")'
            _, messages = self.imap.search(None, search_criteria)
            mail_ids = messages[0].split()
            for i, mail_id in enumerate(mail_ids):
                _, msg_data = self.imap.fetch(mail_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                subject = self.decode_mime(msg.get("Subject"))
                from_name, from_addr = parseaddr(msg.get("From"))
                from_name = self.decode_mime(from_name)
                date = msg.get("Date")

                body = self.get_mail_body(msg)

                content = {
                    "subject":subject,
                    "from":f"{from_name} <{from_addr}>",
                    "date":date,
                    "body":body
                }
                result_list.append(content)
            return result_list
        except TimeoutError as e:
            print("IMAP timeout:", e)
            return []   

        except Exception as e:
            print("Mail error:", e)
            return []
    
    @staticmethod
    def decode_mime(s):
        if not s:
            return ""
        parts = decode_header(s)
        result = []
        for text, enc in parts:
            if isinstance(text, bytes):
                result.append(text.decode(enc or "utf-8", errors="ignore"))
            else:
                result.append(text)
        return "".join(result)
    
    @staticmethod
    def get_mail_body(msg):
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get("Content-Disposition"))

                if ctype == "text/plain" and "attachment" not in disp:
                    return part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8",
                        errors="ignore"
                    )

            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    return part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8",
                        errors="ignore"
                    )
        else:
            body = msg.get_payload(decode=True).decode(
                msg.get_content_charset() or "utf-8",
                errors="ignore"
            )

        return body
from src.engine.mail_engine import MailEngine

mail_service = MailEngine()
result = mail_service.pull_mails()
for x in result:
    print(x)
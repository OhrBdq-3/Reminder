from engine.mail_engine import MailEngine
from engine.model_engine import ChatEngine
import json
from utils.helper import  handle_failed_ai_response

def convert_mails_to_reminder(ai_engine: ChatEngine):
    try:
        mail_engine = MailEngine()
        results = mail_engine.pull_mails()
        parsed_result_list = []
        for mail in results:
            parsed_result = ai_engine.get_json_response(
                content = json.dumps(mail)
            )
            parsed_result_list.append(parsed_result)
        return parsed_result_list
    except:
        handle_failed_ai_response()
        

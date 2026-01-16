from config.reminder_schema import REMINDER_SCHEMA  
from config.tone_prompt import TONE_MAP
from utils.helper import load_setting, handle_failed_ai_response, get_app_data_path
import json
import traceback, os

class ChatEngine:
    def __init__(self,):
        self.client = None
        self.model_info = None

    def _ensure_initialized(self):
        if self.client is None:
            from openai import OpenAI 
            self.model_info = self._load_config()
            self.client = OpenAI(
                api_key=self.model_info["api_key"],
            )

    def _load_config(self) -> dict:
        config = load_setting().get("ai_setting")
        enable_ai = config.get("enable_ai")
        if enable_ai:
            required = ["api_base_url", "current_model", "api_key"]
            for k in required:
                if k not in config:
                    raise ValueError(f"Missing config field: {k}")
        return config

    def get_response(self, content: str):
        responses = self.client.chat.completions.create(
            model=self.model_info["current_model"],
            messages=[{"role": "user", "content": content}],
            stream=True,
        )
        for chunk in responses:
                if chunk.choices[0].delta.content:
                    for char in chunk.choices[0].delta.content:
                        yield char

    def get_json_response(self, content:str, tone: str = 'default'):
        try:
            self._ensure_initialized() 
            response = self.client.chat.completions.parse(
                model=self.model_info["current_model"],
                messages=[
                    {
                        "role": "system",
                        "content": TONE_MAP.get(tone, "default")
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "reminder",
                        "schema": REMINDER_SCHEMA
                    }
                }
            )
            
            parsed_result = json.loads(response.choices[0].message.content)
            return parsed_result
        except Exception as e:
            # 打包后看不到控制台，所以我们将错误写进一个本地文件

            log_path = os.path.join(get_app_data_path(), "ai_debug_log.txt")
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(f"Error Type: {type(e).__name__}\n")
                f.write(f"Error Message: {str(e)}\n")
                f.write(traceback.format_exc())
            
            # 同时也返回失败处理
            return handle_failed_ai_response()

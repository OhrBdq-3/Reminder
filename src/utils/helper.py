import os
import json
from datetime import datetime

def get_app_data_path():
    # 获取 C:\Users\用户名\AppData\Roaming\MyReminderApp
    app_data_dir = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "MyReminderApp")
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)
    return app_data_dir

# 修复后的配置文件路径
SETTING_PATH = os.path.join(get_app_data_path(), 'setting.json')
print(SETTING_PATH)
def load_setting(path = SETTING_PATH):
    if not os.path.exists(path):
        with open(path,'w',encoding = 'utf-8') as f:
            json.dump({}, f)
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load setting:", e)
        return {}
    
def write_setting(config, path = SETTING_PATH):
    with open(path,'w',encoding='utf-8') as f:
        json.dump(config, f,indent=2)

def handle_failed_ai_response():
    return {'title': 'Couldn’t generate reminder', 
            'description': 'AI couldn’t connect. You can edit this reminder manually.', 
            'datetime': datetime.now().strftime("%H:%M:%S"), 
            'option': 'Today'}
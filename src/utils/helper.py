import os
import json

SETTING_PATH = os.path.join(os.getcwd(),'src','config','setting.json')

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
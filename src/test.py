from engine.model_engine import ChatEngine


if __name__ == "__main__":
    chat_engine =ChatEngine()
    content = "今天上午11点汇报"
    chat_engine.get_json_response(content)
    basetime = content.get("datetime")
    #datetime.strptime(base_time, "%H:%M:%S").time()
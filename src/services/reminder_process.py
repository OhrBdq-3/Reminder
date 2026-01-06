from datetime import datetime, date, timedelta
from models.reminder import Reminder

def is_workday(d: date):
    return d.weekday() < 5   # 0-4

def is_weekend(d: date):
    return d.weekday() >= 5  # 5,6

def create_reminder(id: str, 
                    title: str, 
                    base_time: str, 
                    description: str, 
                    option: str) -> Reminder:
    today = date.today()
    if title == '':
        title = "Just Remind Me"

    if option == "Today":
        trigger_date = today
        repeat = "none"

    elif option == "Tomorrow":
        trigger_date = today + timedelta(days=1)
        repeat = "none"

    elif option == "Daily":
        trigger_date = today
        repeat = "daily"

    elif option == "Workdays":
        d = today
        while not is_workday(d):
            d += timedelta(days=1)
        trigger_date = d
        repeat = "workdays"

    elif option == "Weekend":
        d = today
        while not is_weekend(d):
            d += timedelta(days=1)
        trigger_date = d
        repeat = "weekend"
    base_time_parsed = datetime.strptime(base_time, "%H:%M:%S").time()
    next_trigger_time = datetime.combine(trigger_date, base_time_parsed)

    return Reminder(
        id=id,
        title=title,
        base_time=base_time_parsed,
        next_trigger_time=next_trigger_time,
        description=description,
        status="pending",
        option=option,
        repeat=repeat,
    )

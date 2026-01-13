from dataclasses import dataclass
from datetime import time, datetime
from enum import Enum


class ReminderStatus(Enum):
    PENDING = "pending"
    DONE = "done"
    EXPIRED = "expired"

class OptionType(Enum):
    TODAY = "Today"
    TOMORROW = "Tomorrow"
    DAILY = "Daily"
    WORKDAYS = "Workdays"
    WEEKEND = "Weekend"

class RepeatType(Enum):
    NONE = "none"
    DAILY = "daily"
    WORKDAYS = "workdays"
    WEEKEND = "weekend"

@dataclass
class Reminder:
    id: str 
    title: str
    base_time: time
    next_trigger_time: datetime 
    description: str = ""
    status: ReminderStatus = ReminderStatus.PENDING
    option: OptionType  = OptionType.TODAY
    repeat: RepeatType = RepeatType.NONE
    is_snoozed: int = 0
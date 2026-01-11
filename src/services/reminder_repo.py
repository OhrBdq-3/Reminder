import sqlite3
from pathlib import Path
from models.reminder import Reminder
import os
from datetime import datetime


DB_PATH = os.path.join(os.getcwd(),"src","data/reminders.db")


class ReminderRepository:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            base_time TEXT NOT NULL,
            next_trigger_time TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            option TEXT NOT NULL,
            repeat TEXT NOT NULL,
            IS_SNOOZED BOOLEAN NOT NULL DEFAULT 0
        )
        """)
        self.conn.commit()

    def add(self, reminder: Reminder) -> Reminder:
        self.conn.execute(
            """INSERT INTO reminders 
                (id, title, base_time, next_trigger_time, description, status, option, repeat, is_snoozed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(reminder.id),
                reminder.title, 
                reminder.base_time.strftime("%H:%M:%S"), 
                reminder.next_trigger_time.strftime("%Y-%m-%d %H:%M:%S"), 
                reminder.description, 
                reminder.status, 
                reminder.option, 
                reminder.repeat,
                reminder.is_snoozed
            )
        )
        self.conn.commit()
        return reminder

    def list_all(self) -> list[Reminder]:
        rows = self.conn.execute("SELECT * FROM reminders").fetchall()
        return [
            Reminder(
                id=row["id"],
                title=row["title"],
                base_time=datetime.strptime(row["base_time"],"%H:%M:%S"),
                next_trigger_time=datetime.strptime(row["next_trigger_time"],"%Y-%m-%d %H:%M:%S"),
                description=row["description"],
                status = row["status"],
                option = row["option"],
                repeat = row["repeat"],
                is_snoozed=row["is_snoozed"]
            )
            for row in rows
        ]

    def delete(self, reminder_id: int):
        self.conn.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        self.conn.commit()

    def update(self, reminder: Reminder):
        self.conn.execute(
            """update reminders set 
                title = ?, 
                base_time = ?, 
                next_trigger_time = ?, 
                description = ?, 
                status = ?, 
                option = ?, 
                repeat = ?, 
                is_snoozed = ?  
                where id = ?
            """
        ,(reminder.title, reminder.base_time.strftime("%H:%M:%S"), reminder.next_trigger_time.strftime("%Y-%m-%d %H:%M:%S"), reminder.description, reminder.status, reminder.option, reminder.repeat, reminder.is_snoozed, reminder.id))
        self.conn.commit()
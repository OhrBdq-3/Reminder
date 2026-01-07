from ui.views.reminder_toast import ReminderToast
import flet as ft
from datetime import datetime, timedelta

class NotificationManager:
    def __init__(self, page, repo, on_refresh):
        self.page = page
        self.repo = repo
        self.on_refresh = on_refresh
        self.toast_column = ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.END,
        )

        self.stack = ft.Stack(
            expand=True,
            alignment=ft.alignment.bottom_right,
            right=0,
            bottom=0,
            controls=[
                ft.Container(
                    padding=20,
                    content=self.toast_column
                )
            ],
        )

        self.page.overlay.append(self.stack)
        self.page.update()

    def show(self, reminder):
        toast = ReminderToast(
            reminder=reminder,
            on_done=self._on_done,
            on_snooze=self._on_snooze,
        )
        self.toast_column.controls.append(toast)
        self.page.update()

    def _on_done(self, reminder):
        if reminder.repeat == "none":
            reminder.status = "done"
        else:
            self._after_triggered(reminder)
        reminder.is_snoozed = 0
        self.repo.update(reminder)
        self._remove(reminder)
        self.on_refresh()

        print(f"Done: {reminder.title}")

    def _on_snooze(self, reminder):
        reminder.next_trigger_time = datetime.now() + timedelta(minutes=10)
        reminder.is_snoozed = 1
        reminder.status = "pending"
        self.repo.update(reminder)
        self._remove(reminder)
        self.on_refresh()

        print(f"Snoozed: {reminder.title}")

    def _remove(self, reminder):
        for c in list(self.toast_column.controls):
            if c.reminder.id == reminder.id:
                self.toast_column.controls.remove(c)
        self.page.update()


    def _after_triggered(self,reminder):
        if reminder.repeat == "none":
            reminder.status = "done"

        elif reminder.repeat == "daily":
            reminder.next_trigger_time += timedelta(days=1)
        
        elif reminder.repeat == "workdays":
            d = reminder.next_trigger_time
            while True:
                d += timedelta(days = 1)
                if d.weekday() < 5:
                    break
            reminder.next_trigger_time = d
        
        elif reminder.repeat == "weekend":
            d = reminder.next_trigger_time
            while True:
                d += timedelta(days = 1)
                if d.weekday() >= 5:
                    break
            reminder.next_trigger_time = d
        self.repo.update(reminder)
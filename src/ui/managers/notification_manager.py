from ui.views.reminder_toast import ReminderToast
import flet as ft


class NotificationManager:
    def __init__(self, page, on_refresh):
        self.page = page
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
        self._remove(reminder)
        self.on_refresh()
        self.page.update()
        print(f"Done: {reminder.title}")

    def _on_snooze(self, reminder):
        self._remove(reminder)
        self.on_refresh()
        self.page.update()
        print(f"Snoozed: {reminder.title}")

    def _remove(self, reminder):
        for c in list(self.toast_column.controls):
            if c.reminder.id == reminder.id:
                self.toast_column.controls.remove(c)
        self.page.update()


import flet as ft

class ReminderToast(ft.Container):
    def __init__(self, reminder, on_done = None, on_snooze = None):
        super().__init__()
        self.reminder = reminder
        self.content = ft.Column(
            spacing = 8,
            controls = [
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls = [
                        ft.Row(
                            controls = [
                                ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE_OUTLINED, color = ft.Colors.AMBER_800),
                                ft.Text(reminder.title, weight = ft.FontWeight.BOLD, size=16)
                            ],
                            spacing = 8,
                        )
                    ]
                ),
                ft.Text(
                    reminder.base_time.strftime('%H:%M') + ' @ ' + reminder.option,
                    size = 12,
                    color = ft.Colors.ON_SURFACE_VARIANT
                ),
                ft.Text(
                    reminder.description or "No description provided",
                    size=13,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.TextButton("Done", on_click=lambda e: on_done(reminder)),
                        ft.TextButton("Snooze", on_click=lambda e: on_snooze(reminder)),
                    ],
                ),
            ]
        )
        self.width = 300
        self.height = 150
        self.padding = 12
        self.border_radius = 12
        self.bgcolor = ft.Colors.SURFACE
        self.shadow = ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12)

    def _animate(self):
        self.opacity = 0 if self.opacity == 1 else 1
        self.update()
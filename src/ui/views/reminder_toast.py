import flet as ft

class ReminderToast(ft.Container):
    def __init__(self, 
                 reminder, 
                 on_done = None, 
                 on_snooze = None):
        super().__init__()
        self.reminder = reminder
        self.on_done = on_done
        self.on_snooze = on_snooze
        self.content = ft.Column(
            spacing = 8,
            controls = [
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.NOTIFICATIONS_ACTIVE_OUTLINED, color=ft.Colors.AMBER_800),
                                ft.Text(
                                    reminder.title, 
                                    weight=ft.FontWeight.BOLD, 
                                    size=16,
                                    # 关键 1：允许换行
                                    no_wrap=False, 
                                    # 关键 2：确保它在 Row 中占用剩余所有空间
                                    expand=True, 
                                )
                            ],
                            spacing=8,
                            # 关键 3：让图标对齐文字顶端，防止文字多行时图标居中
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            # 关键 4：给这个内部 Row 也设置 expand，让它填满外部 Row
                            expand=True 
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
                        ft.TextButton("Done", on_click=lambda e, r=reminder: self.on_done(r)),
                        ft.TextButton("Snooze", on_click=lambda e, r=reminder: self.on_snooze(r)),
                    ],
                ),
            ]
        )
        self.width = 300
        #self.height = 150
        self.padding = 12
        self.border_radius = 12
        self.bgcolor = ft.Colors.SURFACE
        self.shadow = ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12)

    def _animate(self):
        self.opacity = 0 if self.opacity == 1 else 1
        self.update()
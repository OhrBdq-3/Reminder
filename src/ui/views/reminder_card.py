import flet as ft
from ui.views.edit_dialog import EditField

class ReminderCard(ft.Card):
    def __init__(self, reminder,
                 on_delete = None,
                 on_edit = None,
                ):
        
        super().__init__()
        self.elevation = 2
        self.reminder = reminder
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.description_text = ft.Text(self.reminder.description, expand=True, selectable=True, size = 13, color = ft.Colors.GREY_700,) if self.reminder.description else None
        self.option = self.reminder.option
        self.is_snoozed = reminder.is_snoozed

        if self.reminder.status == "pending":
            if self.reminder.is_snoozed == 0:
                self.status_color = ft.Colors.BLUE_900
                self.leading_icon = ft.Icons.ALARM
            else:
                self.status_color = ft.Colors.RED_800
                self.leading_icon = ft.Icons.SNOOZE_OUTLINED
        elif self.reminder.status == "done":
            self.status_color = ft.Colors.GREEN_900
            self.leading_icon = ft.Icons.AUTO_AWESOME_OUTLINED
        elif self.status_color == "expired":
            self.status_color = ft.Colors.RED_900
            self.leading_icon = ft.Icons.DANGEROUS_OUTLINED
        else:
            self.status_color = ft.Colors.BLUE_900
            self.leading_icon = ft.Icons.ALARM

        self.chip_status = self.reminder.status.capitalize() if self.reminder.is_snoozed == 0 else "Snoozed"
        self.pending_hint = ft.Chip(
            label = ft.Text(self.chip_status, width = 60, text_align=ft.TextAlign.CENTER),
            label_style=ft.TextStyle(color=self.status_color, weight= ft.FontWeight.W_700)
        )
        self.up_title = self.reminder.title.title()
        self.title_row = ft.Row(
            controls = [
                ft.Text(self.up_title or "Just Remind Me", size=18, weight=ft.FontWeight.BOLD, selectable=True),
                self.pending_hint
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

        if self.is_snoozed:
            self.time_display = ft.Text(
                self.option + " · " + 'Snoozed to ' + self.reminder.next_trigger_time.strftime("%H:%M"),
                size=13,
                weight=ft.FontWeight.W_500
            )
        else:
            self.time_display = ft.Text(
                self.option + " · " + self.reminder.base_time.strftime("%H:%M"),
                size=13,
                weight=ft.FontWeight.W_500
            )
        self.card_content = ft.ListTile(
            leading = ft.Icon(self.leading_icon, size = 30, color =self.status_color),
            title = self.title_row,
            subtitle = ft.Column(
                controls = [
                    ft.Row(
                                [
                                    self.time_display
                                ],
                                spacing=6
                            ),
                    self.description_text or ft.Text("No description provided"), 
                ], spacing = 4
            )
        )

        self.edit_btn = ft.IconButton(
            icon=ft.Icons.EDIT_OUTLINED,
            icon_color=ft.Colors.GREY_600,
            tooltip="Edit",
            on_click=self.handle_edit
        )

        self.delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color=ft.Colors.GREY_600,
            tooltip="Delete",
            on_click=self.handle_delete
        )
        self.actions = ft.Row(
            controls=[
                self.edit_btn,
                self.delete_btn
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing = 4,
            opacity=0.0,
            animate_opacity=300,
            animate_offset=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
        )

        self.main_column = ft.Column(
            controls = [
                self.card_content,
                self.actions
            ]
        )

        self.main_container = ft.Container(
            content = self.main_column,
            padding = 10,
            on_hover= self.on_hover
        )

        self.content = self.main_container
        self.margin = 10

    def handle_delete(self, e):
        if self.on_delete:
            self.on_delete(self.reminder)

    def handle_edit(self, e):
        if self.on_edit:
            self.on_edit(self.reminder)

    def on_hover(self, e):
        is_hovered = e.data == "true"
        self.actions.opacity = 1.0 if is_hovered else 0.0
        self.actions.update()

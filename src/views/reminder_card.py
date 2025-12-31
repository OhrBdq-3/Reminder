import flet as ft

class ReminderCard(ft.Card):
    def __init__(self, 
                 reminder_name: str, 
                 reminder_time: str, 
                 description: str = None,
                 on_delete = None,
                 on_edit = None
                ):
        
        super().__init__()
        self.reminder_name = reminder_name
        self.reminder_time = reminder_time
        self.description = description
        self.on_delete = on_delete
        self.on_edit = on_edit 
        self.description_text = ft.Text(self.description, expand=True) if self.description else None

        self.card_content = ft.ListTile(
            leading = ft.Icon(ft.Icons.ALARM),
            title = ft.Text(self.reminder_name or "Just Remind Me", size=16, weight=ft.FontWeight.BOLD, selectable=True),
            subtitle = ft.Column(
                controls = [
                    ft.Text(f"Time: {self.reminder_time}", size=12, selectable=True),
                    ft.Text(self.description or "No description provided", selectable=True),
                ]
            )
        )

        self.delete_btn = ft.TextButton(
            text = "Delete",
            icon = ft.Icons.DELETE,
            on_click=self.handle_delete
        )

        self.edit_btn = ft.TextButton(
            text = "Edit",
            icon = ft.Icons.EDIT,
        )

        self.actions = ft.Row(
            controls=[
                self.edit_btn,
                self.delete_btn
            ],
            alignment=ft.MainAxisAlignment.END
        )

        self.main_column = ft.Column(
            controls = [
                self.card_content,
                self.actions
            ]
        )

        self.main_container = ft.Container(
            content = self.main_column,
            padding = 10
        )

        self.content = self.main_container
        self.margin = 10

    def handle_delete(self, e):
        if self.on_delete:
            self.on_delete(self)
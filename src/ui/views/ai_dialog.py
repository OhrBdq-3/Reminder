import flet as ft
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from utils.helper import load_setting

ai_executor = ThreadPoolExecutor(max_workers=2)

class AIDialog(ft.AlertDialog):
    def __init__(self, page, on_parsed = None, on_submit=None, on_update = None):
        super().__init__()
        self._page = page
        self.on_submit = on_submit
        self.on_parsed = on_parsed
        self.on_update = on_update
        self.title = ft.Text("New Reminder", weight=ft.FontWeight.BOLD, size = 18)

        self.title_text = ft.Text("Powered by AI", size = 12, color = ft.Colors.ON_SURFACE_VARIANT)
        self.inbox_textfield = ft.TextField(
            label="Describe your needs",
            on_submit=self.handle_submit,
            multiline=True,
            shift_enter = True,
            min_lines=3,
            autofocus=True,
        )

        self.add_btn = ft.IconButton(
            icon = ft.Icons.CHECK,
            tooltip="Add Reminder",
            on_click = self.handle_submit,
            icon_color=ft.Colors.BLACK
        )

        self.cancel_btn = ft.IconButton(
            icon = ft.Icons.CANCEL,
            tooltip="Cancel",
            on_click = self.cancel_submit,
            icon_color=ft.Colors.BLACK
        )

        self.actions_btns = ft.Row(
            controls = [
                self.cancel_btn,
                self.add_btn
            ],
        )

        self.input_column = ft.Column(
            tight=True,
            spacing=10,
            controls = [
                self.title_text,
                self.inbox_textfield,
            ],
            
        )
        self.actions_row = ft.Row(    
            controls=[self.actions_btns],
            alignment=ft.MainAxisAlignment.END,  
        )
        self.main_column = ft.Column(
            controls = [
                self.input_column,
                self.actions_row
            ],
            expand=True,
            tight=True  
        )
        
        self.main_row = ft.Row(
            controls=[self.main_column],
            expand=True
        )
        
        self.content = ft.Container(
            content=self.main_row,
            padding=20,
            width=380,
        )
        self._page.overlay.append(self)

    def handle_submit(self, e):
        if self.on_submit:
            placeholder = self.on_submit(
                name="Generating...",
                time=datetime.now().time().strftime("%H:%M:%S"),
                description="AI is working...",
                option="Tomorrow",
        )
        ai_executor.submit(
            self._parse_ai_task,
            self.inbox_textfield.value,
            placeholder
        )

        self.close(e)

    def _parse_ai_task(self, text, placeholder):
        tone = load_setting().get("ai_setting").get("tone","default")
        result = self.on_parsed(text, tone)
        self._page.run_thread(
            self._apply_ai_result,
            placeholder,
            result
        )
        self._page.update()


    def _apply_ai_result(self, placeholder, result):
        if self.on_update:
            self.on_update(
                placeholder,
                result.get("title", ""),
                result.get("datetime", ""),
                result.get("description", ""),
                result.get("option", ""),
            )
        self._page.update()

    def cancel_submit(self, e):
        if self.cancel_submit:
            self.close(e)
            self.update()


    def close(self, e):
        self.open = False
        self.update()

    def reset_form(self):        
        self.inbox_textfield.value = ""

    def open_dialog(self, e):
        self.reset_form()
        self.open = True
        self._page.update()
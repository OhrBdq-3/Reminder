import flet as ft
from datetime import time
import datetime
from views.reminder_card import ReminderCard


class InputField(ft.AlertDialog):
    def __init__(self, page: ft.Page, on_submit=None):
        super().__init__()
        self.page_ref = page 
        self.on_submit = on_submit
        self.title = ft.Text("New Reminder")
        self.actions = []

        self.time_input = ft.TimePicker(
            value=datetime.datetime.now().time(),
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            on_change=self.on_time_change 
        )
        
        self.page_ref.overlay.append(self.time_input)

        self.reminder_input = ft.TextField(
            label="Reminder Name",
            hint_text="Enter reminder name",
            on_submit=self.handle_submit
        )
        self.description_input = ft.TextField(
            label="Description",
            hint_text="Enter description",
            on_submit=self.handle_submit
        )

        self.time_display = ft.TextField(
            label="Selected Time",
            value=datetime.datetime.now().time().strftime("%H:%M"),
            read_only=True, 
        )
        
        self.pick_time_btn = ft.IconButton(
            icon = ft.Icons.ACCESS_TIME,
            on_click= self.show_time_picker
        )

        self.add_button = ft.TextButton("Add Reminder", icon = ft.Icons.ADD, on_click=self.handle_submit)
        self.cancel_button = ft.TextButton("Cancel", icon = ft.Icons.CANCEL, on_click=self.cancel_submit)
        self.main_column = ft.Column(
            controls=[
                self.reminder_input,
                self.description_input,
                ft.Row([self.time_display, self.pick_time_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([self.add_button, self.cancel_button])
            ],
            expand=True
        )
        
        self.main_row = ft.Row(
            controls=[self.main_column],
            expand=True
        )
        
        self.content = ft.Container(
            content=self.main_row,
            padding=10,
            width=400,
            height=400
        )

    def on_time_change(self, e):
        # 更新显示的文本框
        time_val = self.time_input.value
        if time_val:
            self.time_display.value = time_val.strftime("%H:%M")
            self.time_display.update()

    def handle_submit(self, e):
        if self.on_submit:
            self.on_submit(
                self.reminder_input.value,
                self.time_input.value, 
                self.description_input.value
            )

        self.reminder_input.value = ""
        self.time_input.value = time(0, 0)
        self.time_display.value = "00:00"
        self.description_input.value = ""
        self.open = False
        self.page_ref.update()

    def cancel_submit(self, e):
        if self.cancel_submit:
            self.open = False
            self.page_ref.update()

    def show_time_picker(self, e):
        self.time_input.open = True
        self.time_input.update()
        

def main(page: ft.Page):
    page.title = "Desktop Assistant - Reminder Module"
    cards = ft.Column()
    title = ft.Text("Reminders", size=24, weight=ft.FontWeight.BOLD)
    page.add(title)


    def delete_card(card):
        cards.controls.remove(card)
        page.update()

    def add_card(reminder_name, reminder_time, description):
        new_card = ReminderCard(
            reminder_name,
            reminder_time,
            description,
            on_delete=delete_card,
        )
        cards.controls.append(new_card)
        page.update()

    input_field = InputField(page, on_submit=add_card)
    
    def open_input_dialog(e):
        page.open(input_field)
        page.update()

    add_button = ft.TextButton(
        text = "Add Reminder",
        icon=ft.Icons.ADD,
        on_click=open_input_dialog
    )

    
    page.add(cards)
    page.add(add_button)



ft.app(main)
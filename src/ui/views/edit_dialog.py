import flet as ft
import datetime

class EditField(ft.AlertDialog):
    def __init__(self, old_reminder, on_submit=None):
        super().__init__()
        self.old_reminder = old_reminder
        self.on_submit = on_submit
        self.title = ft.Text("Edit Reminder", weight=ft.FontWeight.BOLD, size = 18)

        self.title_text = ft.Text("Edit reminder name", size = 12, color = ft.Colors.ON_SURFACE_VARIANT)

        self.title_textfield = ft.TextField(
            value=self.old_reminder.title,
            label = "Rminder title",
            on_submit=self.handle_submit,
            autofocus=True,
        )
        self.pick_time_btn = ft.IconButton(
            icon = ft.Icons.ACCESS_TIME,
            tooltip="Pick Time",
            on_click= self.show_time_picker,
            icon_size=20
        )

        self.time_display = ft.TextField(
            label="Time",
            value = self.old_reminder.base_time.strftime("%H:%M"),
            read_only=True, 
            width=110,
            on_focus=self.show_time_picker,
            on_submit=self.handle_submit,
        )
       # print(self.old_reminder.base_time.strftime("%H:%M"))
        self.time_input = ft.TimePicker(
            value=self.old_reminder.base_time,
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            on_change=self.on_time_change,
            time_picker_entry_mode = ft.TimePickerEntryMode.INPUT
        )

        self.day_picker = ft.Dropdown(
            value = self.old_reminder.option,
            options = [
                ft.dropdown.Option("Today"),
                ft.dropdown.Option("Tomorrow"),
                ft.dropdown.Option("Daily"),
                ft.dropdown.Option("Workdays"),
                ft.dropdown.Option("Weekend"),
            ],
            label="Remind me on",
            width = 180,
        )

        
        self.time_row = ft.Row(
            [
                self.time_display, 
                self.day_picker
            ], 
            spacing = 8
        )

        self.description_input = ft.TextField(
            label="Notes (optional)",
            min_lines=1,
            max_lines=3,
            on_submit=self.handle_submit,
            value=self.old_reminder.description
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
                self.title_textfield,
                self.time_row,
                self.description_input,
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

    def on_time_change(self, e):
        time_val = self.time_input.value
        if time_val:
            self.time_display.value = time_val.strftime("%H:%M")
            self.time_display.update()
            self.time_input.open = False
            self.time_input.update()

    def handle_submit(self, e):
        if self.on_submit:
            self.on_submit(
                self.title_textfield.value,
                str(self.time_input.value), 
                self.description_input.value,
                self.day_picker.value,
            )

        self.close(e)


    def cancel_submit(self, e):
        if self.cancel_submit:
            self.close(e)
            self.update()

    def show_time_picker(self, e):
        self.time_input.open = True
        self.time_input.update()

    def close(self, e):
        self.open = False
        self.update()
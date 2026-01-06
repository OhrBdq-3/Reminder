import flet as ft
from services.reminder_repo import ReminderRepository
from ui.views.reminder_card import ReminderCard
from ui.views.input_dialog import InputField
from uuid import uuid4
from services.reminder_scheduler import ReminderScheduler
from ui.managers.notification_manager import NotificationManager
from services.reminder_process import create_reminder


repo = ReminderRepository()

def main(page: ft.Page):
    page.title = "Desktop Assistant - Reminder Module"
    cards = ft.ListView(
        spacing=10,
        padding=10,
        auto_scroll=True,
        expand=True
    )
    def load_reminders():
        cards.controls.clear()
        reminders = repo.list_all()
        for rem in reminders:
            card = ReminderCard(
                reminder = rem,
                on_delete=lambda e, rem = rem: delete_reminder(rem)
            )
            cards.controls.append(card)
        page.update()

    load_reminders()
    notification_manager = NotificationManager(page = page, on_refresh=load_reminders)
    
    def on_reminder_triggered(reminder):
        notification_manager.show(reminder)
        print(f"Reminder: {reminder.title} @ {reminder.base_time}")
        
    
    scheduler = ReminderScheduler(
        repo = repo,
        on_trigger= on_reminder_triggered
    )
    scheduler.start()

    def delete_reminder(reminder):
        repo.delete(reminder.id)
        cards.controls[:] = [
            c for c in cards.controls if c.reminder.id != reminder.id
        ]
        page.update()


    title = ft.Text("Reminders", size=24, weight=ft.FontWeight.BOLD)
    page.add(title)

    def add_card(reminder_name, reminder_time, description, option):
        new_data = create_reminder(
                id=str(uuid4()),
                title=reminder_name,
                base_time=reminder_time,
                description=description,
                option=option
            )

        new_card = ReminderCard(
            reminder = new_data,
            on_delete=lambda e, rem = new_data: delete_reminder(rem)
        )
        cards.controls.append(new_card)
        print(new_data)
        repo.add(new_data)
        page.update()
        
    input_field = InputField(on_submit=add_card)

    page.overlay.append(input_field.time_input)

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

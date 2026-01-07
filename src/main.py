import flet as ft
from services.reminder_repo import ReminderRepository
from ui.views.reminder_card import ReminderCard
from ui.views.input_dialog import InputField
from ui.views.edit_dialog import EditField
from uuid import uuid4
from services.reminder_scheduler import ReminderScheduler
from ui.managers.notification_manager import NotificationManager
from services.reminder_process import create_reminder
from ui.views.side_bar import SideBar


repo = ReminderRepository()

def main(page: ft.Page):
    page.title = "Desktop Assistant - Reminder Module"

    cards = ft.ListView(
        spacing=10,
        padding=10,
        auto_scroll=True,
        expand=True
    )
    rail = SideBar()
    
    def load_reminders():
        cards.controls.clear()
        reminders = repo.list_all()
        for rem in reminders:
            card = ReminderCard(
                reminder = rem,
                on_delete=lambda e, rem = rem: delete_reminder(rem),
                on_edit=lambda e, rem = rem: open_edit_dialog(rem),
            )
            cards.controls.append(card)
        page.update()

    load_reminders()
    notification_manager = NotificationManager(page = page, repo = repo, on_refresh=load_reminders)
    
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

    def edit_reminder(reminder, new_title, new_base_time, new_description, new_option):
        reminder.title = new_title
        reminder.base_time = new_base_time
        reminder.description = new_description
        reminder.option = new_option

        updated = create_reminder(
            id=reminder.id,
            title=new_title,
            base_time=new_base_time,
            description=new_description,
            option=new_option
        )

        reminder.next_trigger_time = updated.next_trigger_time
        reminder.base_time = updated.base_time
        reminder.repeat = updated.repeat
        reminder.status = "pending"
        repo.update(reminder)
        load_reminders()
    
    def open_edit_dialog(old_reminder):
        print('here')
        edit_field = EditField(
            old_reminder=old_reminder,
            on_submit=lambda title, time, desc, opt:
                edit_reminder(old_reminder, title, time, desc, opt)
        )
        page.overlay.append(edit_field.time_input)
        page.open(edit_field)
        page.update()
        

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
            on_delete=lambda e, rem = new_data: delete_reminder(rem),
            on_edit=lambda e, rem = new_data: open_edit_dialog(rem),
        )
        cards.controls.append(new_card)
        print(new_data)
        repo.add(new_data)
        page.update()


    input_field = InputField(on_submit=add_card)

    page.overlay.append(input_field.time_input)

    def open_input_dialog(e):
        input_field.reset_form()
        page.open(input_field)
        page.update()

    add_button = ft.TextButton(
        text = "Add Reminder",
        icon=ft.Icons.ADD,
        on_click=open_input_dialog
    )
    
    main_row = ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            cards
        ],
        expand=True
    )
    page.add(main_row)
    page.add(add_button)



ft.app(main)

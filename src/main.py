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
from ui.managers.theme_manager import ThemeManager
from ui.views.card_list import CardList
from ui.managers.cardlist_manager import CardListManager

repo = ReminderRepository()

def main(page: ft.Page):
    page.title = "Desktop Assistant - Reminder Module"
    page.theme_mode = ft.ThemeMode.LIGHT

    theme_manager = ThemeManager(page = page)
    rail = SideBar(on_change_theme=theme_manager.change_theme)
    card_list_manager = CardListManager(repo = repo, page = page)
    card_list = CardList(page = page, manager=card_list_manager)
    
    card_list.reload()
    
    notification_manager = NotificationManager(page = page, repo = repo, on_refresh=card_list.reload)
    scheduler = ReminderScheduler(
        repo = repo,
        on_trigger= notification_manager.show
    )
    scheduler.start()

    input_field = InputField(page = page, on_submit=card_list.add_card)
    page.overlay.append(input_field.time_input)
    add_button = ft.TextButton(
        text = "Add Reminder",
        icon=ft.Icons.ADD,
        on_click=input_field.open_dialog
    )
    
    main_row = ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            card_list
        ],
        expand=True
    )
    page.add(main_row)
    page.add(add_button)



ft.app(main)

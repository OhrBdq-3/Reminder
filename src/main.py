import flet as ft
from services.reminder_repo import ReminderRepository
from ui.views.input_dialog import InputField
from services.reminder_scheduler import ReminderScheduler
from ui.managers.notification_manager import NotificationManager
from ui.views.side_bar import SideBar
from ui.views.card_list import CardList
from ui.managers.cardlist_manager import CardListManager
from ui.managers.sidebar_manager import SidebarManager
from ui.views.setting_drawer import SettingDrawer

repo = ReminderRepository()

def main(page: ft.Page):
    page.title = "Desktop Assistant - Reminder Module"
    page.theme_mode = ft.ThemeMode.LIGHT


    setting_sheet = SettingDrawer(page = page)
    sidebar = SideBar(setting_sheet=setting_sheet)
    sidebar_manager = SidebarManager(sidebar=sidebar, page = page)
    sidebar.on_change_theme = sidebar_manager.change_theme
    sidebar.on_nav_change = sidebar_manager.toggle_bar
    sidebar.on_select_dest = sidebar_manager.select_dest

    card_list_manager = CardListManager(repo = repo, page = page)
    card_list = CardList(page = page, manager=card_list_manager, sidebar=sidebar)
    sidebar_manager.card_list = card_list
    
    
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
            sidebar,
            ft.VerticalDivider(width=1),
            card_list
        ],
        expand=True
    )
    page.add(main_row)
    page.add(add_button)



ft.app(main)

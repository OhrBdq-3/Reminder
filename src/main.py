import flet as ft
from services.reminder_repo import ReminderRepository
from ui.views.input_dialog import InputField
from ui.views.ai_dialog import AIDialog
from services.reminder_scheduler import ReminderScheduler
from ui.managers.notification_manager import NotificationManager
from ui.views.side_bar import SideBar
from ui.views.card_list import CardList
from ui.managers.cardlist_manager import CardListManager
from ui.managers.sidebar_manager import SidebarManager
from ui.views.setting_drawer import SettingDrawer
from engine.model_engine import ChatEngine
from utils.helper import load_setting

repo = ReminderRepository()

    

def main(page: ft.Page):
    page.title = "Reminder"
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
    card_list_manager.on_refresh = card_list.reload_by_status
    
    
    card_list.reload_by_status('pending')
    
    notification_manager = NotificationManager(page = page, repo = repo, sidebar=sidebar, on_refresh=card_list.reload_by_status)
    scheduler = ReminderScheduler(
        repo = repo,
        on_trigger= notification_manager.show
    )
    scheduler.start()
    ai_engine = ChatEngine()

    input_field = InputField(page = page, on_submit=card_list.add_card)
    ai_input_field = AIDialog(page = page, on_parsed=ai_engine.get_json_response, on_submit=card_list.add_card, on_update=card_list_manager.update)
    
    page.overlay.append(input_field.time_input)


    def on_add_click(e):
        setting = load_setting()
        if setting.get("enable_ai", False):
            ai_input_field.open_dialog(e)
        else:
            input_field.open_dialog(e)

    add_button = ft.TextButton(
        text = "Add Reminder",
        icon=ft.Icons.ADD,
        on_click=on_add_click
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

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
from ui.views.about import About
from utils.helper import load_setting

repo = ReminderRepository()

    

import flet as ft
import threading # 必须导入
import traceback # 用于打印详细错误
# ... 你的其他 import 保持不变 ...

def main(page: ft.Page):
    page.title = "Reminder"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 1. 定义一个全局异常显示函数
    def show_crash_error(error_msg):
        page.clean()
        page.add(
            ft.Column([
                ft.Icon(ft.Icons.ERROR_OUTLINE, color="red", size=50),
                ft.Text("程序启动失败", size=20, weight="bold"),
                ft.Text(error_msg, color="red", selectable=True)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    try:
        # 2. 基础组件初始化
        about_page = About(page=page)
        setting_sheet = SettingDrawer(page=page)
        
        sidebar = SideBar(setting_sheet=setting_sheet, on_about_click=about_page.open_about)
        sidebar_manager = SidebarManager(sidebar=sidebar, page=page)
        sidebar.on_change_theme = sidebar_manager.change_theme
        sidebar.on_nav_change = sidebar_manager.toggle_bar
        sidebar.on_select_dest = sidebar_manager.select_dest

        card_list_manager = CardListManager(repo=repo, page=page)
        card_list = CardList(page=page, manager=card_list_manager, sidebar=sidebar)
        sidebar_manager.card_list = card_list
        card_list_manager.on_refresh = card_list.reload_by_status
        
        # 3. 核心管理类
        notification_manager = NotificationManager(page=page, repo=repo, sidebar=sidebar, on_refresh=card_list.reload_by_status)
        
        # --- 重点修改：Scheduler 使用线程启动 ---
        scheduler = ReminderScheduler(
            repo=repo,
            on_trigger=notification_manager.show
        )
        # 使用 daemon=True 确保主程序退出时，子线程也退出
        thread = threading.Thread(target=scheduler.start, daemon=True)
        thread.start() 
        
        ai_engine = ChatEngine()

        input_field = InputField(page=page, on_submit=card_list.add_card)
        ai_input_field = AIDialog(page=page, on_parsed=ai_engine.get_json_response, on_submit=card_list.add_card, on_update=card_list_manager.update)
        
        page.overlay.append(input_field.time_input)

        def on_add_click(e):
            try:
                setting = load_setting()
                if setting.get("enable_ai", False):
                    ai_input_field.open_dialog(e)
                else:
                    input_field.open_dialog(e)
            except Exception as ex:
                print(f"Click Error: {ex}")

        add_button = ft.TextButton(
            text="Add Reminder",
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

        # 4. 先添加布局
        page.add(main_row)
        page.add(add_button)
        
        # 5. 最后异步加载数据，防止阻塞首屏渲染
        card_list.reload_by_status('pending')
        page.update()

    except Exception:
        # 捕获所有初始化阶段的报错并显示
        error_info = traceback.format_exc()
        show_crash_error(error_info)

ft.app(target=main)
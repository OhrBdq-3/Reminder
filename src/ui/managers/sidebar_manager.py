import flet as ft

DEST_MAP = {
    0:'none',
    1:'pending',
    2:'done'
}
class SidebarManager:
    def __init__(self, sidebar, page, card_list = None):
        self.sidebar = sidebar
        self.page = page
        self.card_list = card_list
        self.collapsed = False

    def change_theme(self):
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.sidebar.theme_btn.icon = ft.Icons.DARK_MODE if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE
        self.page.update()

    def toggle_bar(self):
        self.collapsed = not self.collapsed
        self.sidebar.width = 100 if self.collapsed else 220
        self.sidebar.nav.extended = not self.collapsed
        self.sidebar.setting_btn.visible = not self.collapsed
        self.sidebar.about_btn.visible = not self.collapsed
        self.sidebar.menu_btn.tooltip = (
            "Open sidebar" if self.collapsed else "Close sidebar"
        )
        
        self.sidebar.update()

    def select_dest(self, e):
        index = e.control.selected_index
        status = DEST_MAP.get(index)
        if status == 'none':
            self.card_list.reload()
            self.card_list.update()
        else:
            self.card_list.reload_by_status(status)
            self.card_list.update()
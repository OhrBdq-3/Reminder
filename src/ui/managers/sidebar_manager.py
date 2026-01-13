import flet as ft

class SidebarManager:
    def __init__(self, sidebar, page):
        self.sidebar = sidebar
        self.page = page
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

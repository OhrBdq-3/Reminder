import flet as ft

class ThemeManager():
    def __init__(self, page: ft.Page):
        self.page = page
        
    def change_theme(self):
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.page.update()
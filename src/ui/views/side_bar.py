import flet as ft


class SideBar(ft.Container):
    def __init__(self, on_change_theme, on_nav_change = None, on_settings_click = None, on_about_click = None):
        super().__init__()

        self.width = 160
        self.bgcolor = ft.Colors.SURFACE
        self.padding = ft.padding.symmetric(vertical=12)
        self.on_change_theme = on_change_theme
        self.on_nav_change = on_nav_change
        self.on_settings_click = on_settings_click
        self.on_about_click = on_about_click
        
        self.nav = ft.NavigationRail(
            selected_index=1,
            label_type=ft.NavigationRailLabelType.ALL,
            group_alignment=-0.9,
            expand = True,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.LIST_ALT, label="All"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SCHEDULE, label="Upcoming"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SNOOZE, label="Snoozed"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE, label="Completed"
                ),
            ],
            on_change=lambda e: print("Selected destination:", e.control.selected_index),
        )

        self.setting_btn = ft.IconButton(
            icon=ft.Icons.SETTINGS_ROUNDED,
            icon_size = 15
        )
        self.about_btn = ft.IconButton(
            icon = ft.Icons.QUESTION_MARK_ROUNDED,
            icon_size=15
        )
        self.theme_btn = ft.IconButton(
            icon = ft.Icons.DARK_MODE,
            icon_size = 15,
            on_click=self.handle_change_theme
        )
        self.header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.MENU,
                    icon_size=20
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.SEARCH,
                    icon_size=20
                ),
            ],
        )
        self.content = ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=8),
                    content=self.header
                ),
                self.nav,
                ft.Container(expand=True),
                ft.Container(
                    alignment=ft.alignment.center,
                    content = ft.Row(
                        [
                            self.setting_btn,
                            self.about_btn,
                            self.theme_btn
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )

            ],
        )
    def handle_change_theme(self, e):
        if self.on_change_theme:
            self.on_change_theme()
        self.theme_btn.icon = (
            ft.Icons.DARK_MODE
            if self.theme_btn.icon == ft.Icons.LIGHT_MODE
            else ft.Icons.LIGHT_MODE
        )
        self.update()
        
    def handle_click_setting(self, e):
        if self.on_settings_click:
            self.on_settings_click()
    
    def handle_click_about(self, e):
        if self.on_about_click:
            self.on_about_click()
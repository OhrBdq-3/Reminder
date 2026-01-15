import flet as ft


class SideBar(ft.Container):
    def __init__(self, 
                 setting_sheet = None,
                 on_change_theme = None, 
                 on_nav_change = None, 
                 on_settings_click = None, 
                 on_about_click = None, 
                 on_select_dest = None):
        super().__init__()

        self.width = 220
        self.padding = ft.padding.symmetric(vertical=12)
        self.setting_sheet = setting_sheet
        self.on_change_theme = on_change_theme
        self.on_nav_change = on_nav_change
        self.on_settings_click = on_settings_click
        self.on_select_dest = on_select_dest
        self.on_about_click = on_about_click
        self.animate = ft.Animation(260, ft.AnimationCurve.EASE_IN_OUT)
        
        self.nav = ft.NavigationRail(
            selected_index=1,
            group_alignment=-0.9,
            expand = True,
            extended=True,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.LIST_ALT, label="All"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SCHEDULE, label="Upcoming"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE, label="Completed"
                ),
            ],
            on_change=self.handle_select_dest,
        )

        self.setting_btn = ft.IconButton(
            icon=ft.Icons.SETTINGS_ROUNDED,
            icon_size = 15,
            tooltip="Setting",
            on_click = self.setting_sheet.open_drawer
        )
        self.about_btn = ft.IconButton(
            icon = ft.Icons.QUESTION_MARK_ROUNDED,
            icon_size=15,
            tooltip="About",
            on_click = self.handle_click_about
        )
        self.theme_btn = ft.IconButton(
            icon = ft.Icons.DARK_MODE,
            icon_size = 15,
            tooltip="Change theme",
            on_click=self.handle_change_theme
        )
        self.menu_btn = ft.IconButton(
                    icon=ft.Icons.MENU,
                    icon_size=20,
                    tooltip = "Close sidebar",
                    on_click=self.handle_close_nav
                )
        self.header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[self.menu_btn],
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
        
    def handle_close_nav(self,e):
        if self.on_nav_change:
            self.on_nav_change()
        
    def handle_click_setting(self, e):
        if self.on_settings_click:
            self.on_settings_click()
    
    def handle_click_about(self, e):
        if self.on_about_click:
            self.on_about_click()

    def handle_select_dest(self, e):
        if self.on_select_dest:
            self.on_select_dest(e)
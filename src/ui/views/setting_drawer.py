import flet as ft

SNOOZE_OPTIONS = [5, 10, 15, 20, 30, 45, 60]


class SettingDrawer(ft.NavigationDrawer):
    def __init__(self, page: ft.Page, on_save=None):
        super().__init__()

        
        self.page = page
        self.on_save = on_save
        self.selected_snooze = SNOOZE_OPTIONS[1] 

        self.snooze_picker = ft.Dropdown(
            value=str(self.selected_snooze),
            options=[
                ft.dropdown.Option(str(m), f"{m} min")
                for m in SNOOZE_OPTIONS
            ],
            on_change=self.on_snooze_change,
        )

        self.snooze_section = ft.Column(
            spacing=10,
            controls=[
                self._create_section_title("Snooze Time"),
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=10,
                    #border=ft.border.all(1, ft.Colors.OUTLINE),
                    content=self.snooze_picker,
                ),
            ],
        )


        self.enable_gpt = ft.Switch(
            label="Enable AI",
            value=False,
            on_change=self.toggle_gpt_settings,
        )

        self.base_url = ft.TextField(
            label="API Base URL",
            value="https://api.openai.com/v1",
        )

        self.api_key = ft.TextField(
            label="API Key",
            password=True,
            can_reveal_password=True,
        )

        self.model_dropdown = ft.Dropdown(
            label="Current Model",
            value="gpt-4o",
            options=[
                ft.dropdown.Option("gpt-4o"),
                ft.dropdown.Option("claude-3-5-sonnet"),
                ft.dropdown.Option("deepseek-chat"),
            ],
        )

        self.gpt_setting_container = ft.Container(
            visible=False,
            content=ft.Column(
                spacing=15,
                controls=[
                    self._create_section_title("AI Settings"),
                    self.base_url,
                    self.api_key,
                    self.model_dropdown,
                ],
            ),
        )


        self.controls = [
            ft.Container(
                padding=ft.padding.only(top=40, left=20, right=20, bottom=10),
                content=ft.Row(
                    spacing=10,
                    controls=[
                        ft.Icon(ft.Icons.SETTINGS_SUGGEST_ROUNDED, size=30),
                        ft.Text("Setting", size=24, weight=ft.FontWeight.BOLD),
                    ],
                ),
            ),
            ft.Divider(),
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=30,
                    controls=[
                        self.snooze_section,
                        #ft.Divider(),
                        self.enable_gpt,
                        self.gpt_setting_container,
                    ],
                ),
            ),
            ft.Container(
                padding=20,
                content=ft.Row(
                    spacing=10,
                    controls=[
                        ft.OutlinedButton(
                            "Cancel",
                            icon=ft.Icons.CLOSE,
                            on_click=self.close_drawer,
                        ),
                        ft.FilledButton(
                            "Save",
                            icon=ft.Icons.CHECK,
                            expand=True,
                            on_click=self.handle_save,
                        ),
                    ],
                ),
            ),
        ]


    def _create_section_title(self, text: str):
        return ft.Text(
            text,
            size=16,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.BLUE,
        )

    def on_snooze_change(self, e):
        # e.data 是选中的 value，例如 "10"
        self.selected_snooze = int(e.data)

    def toggle_gpt_settings(self, e):
        self.gpt_setting_container.visible = self.enable_gpt.value
        self.page.update()

    def handle_save(self, e):
        config = {
            "snooze": self.selected_snooze,
            "gpt_enabled": self.enable_gpt.value,
            "url": self.base_url.value,
            "key": self.api_key.value,
            "model": self.model_dropdown.value,
        }

        print("Saved config:", config)

        if self.on_save:
            self.on_save(config)

        self.close_drawer()

    def open_drawer(self, e=None):
        self.page.drawer = self
        self.open = True
        self.page.update()

    def close_drawer(self, e=None):
        self.open = False
        self.page.update()

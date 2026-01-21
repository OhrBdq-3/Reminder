import flet as ft
from utils.helper import load_setting, write_setting

SNOOZE_OPTIONS = [5, 10, 15, 20, 30, 45, 60]


class SettingDrawer(ft.NavigationDrawer):
    def __init__(self, page: ft.Page, on_save=None):
        super().__init__(on_dismiss=self._on_dismiss)

        self._page = page
        self.on_save = on_save

        self.setting = load_setting() or {}

        ai_cfg = self.setting.get("ai_setting", {})

        api_base = ai_cfg.get("api_base_url", "https://api.openai.com/v1")
        api_key = ai_cfg.get("api_key", "")
        model_name = ai_cfg.get("model", "gpt-5")
        tone = ai_cfg.get("tone", "default")

        # ---------------- Snooze ----------------
        self.selected_snooze = self.setting.get(
            "snooze_time", SNOOZE_OPTIONS[1]
        )

        self.snooze_picker = ft.DropdownM2(
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
                    padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                    border_radius=10,
                    content=self.snooze_picker,
                ),
            ],
        )

        # ---------------- AI Switch ----------------
        self.enable_gpt = ft.Switch(
            label="Enable AI",
            value=self.setting.get("enable_ai", False),
            on_change=self.toggle_gpt_settings,
        )

        self.base_url = ft.TextField(
            label="API Base URL",
            value=api_base,
        )

        self.api_key = ft.TextField(
            label="API Key",
            password=True,
            can_reveal_password=True,
            value=api_key,
        )

        self.model_dropdown = ft.Dropdown(
            label="Current Model",
            value=model_name,
            options=[
                ft.dropdown.Option("gpt-4o"),
                ft.dropdown.Option("gpt-5.2"),
                ft.dropdown.Option("gpt-5-mini"),
            ],
        )

        self.tone_dropdown = ft.Dropdown(
            label="Tone",
            value=tone,
            options=[
                ft.dropdown.Option("default"),
                ft.dropdown.Option("creative"),
            ],
        )

        self.gpt_setting_container = ft.Container(
            visible=self.setting.get("enable_ai", False),
            content=ft.Column(
                spacing=15,
                controls=[
                    self._create_section_title("AI Settings"),
                    self.api_key,
                    self.model_dropdown,
                    self.tone_dropdown,
                ],
            ),
        )

        # ---------------- Drawer Content ----------------
        self.controls = [
            ft.Container(
                padding=ft.Padding.only(
                    top=40, left=20, right=20, bottom=10
                ),
                content=ft.Row(
                    spacing=10,
                    controls=[
                        ft.Icon(
                            ft.Icons.SETTINGS_SUGGEST_ROUNDED, size=30
                        ),
                        ft.Text(
                            "Setting",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
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

    # ------------------------------------------------
    # Helpers
    # ------------------------------------------------
    def _create_section_title(self, text: str):
        return ft.Text(
            text,
            size=16,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.BLUE,
        )

    # ------------------------------------------------
    # Events
    # ------------------------------------------------
    def on_snooze_change(self, e):
        if self.snooze_picker.value:
            self.selected_snooze = int(self.snooze_picker.value)

    def toggle_gpt_settings(self, e):
        self.gpt_setting_container.visible = self.enable_gpt.value
        self._page.update()

    async def handle_save(self, e):
        config = self.setting.copy()
        config.update(
            {
                "snooze_time": self.selected_snooze,
                "enable_ai": self.enable_gpt.value,
                "ai_setting": {
                    "api_base_url": self.base_url.value,
                    "api_key": self.api_key.value,
                    "model": self.model_dropdown.value,
                    "tone": self.tone_dropdown.value,
                },
            }
        )
        write_setting(config)

        if self.on_save:
            self.on_save(config)

        await self.page.close_drawer()

    # ------------------------------------------------
    # Drawer Control (0.80+ 正确方式)
    # ------------------------------------------------
    async def open_drawer(self, e=None):
        #self._page.show_dialog(self)
        await self.page.show_drawer()
        #self.open = True
        #self._page.update()

    async def close_drawer(self, e=None):
        #self.open = False
        await self.page.close_drawer()
        #self._page.pop_dialog(self)
        #self._page.update()

    def _on_dismiss(self, e):
        print("Drawer dismissed!")
        #self.open = False
        #self._page.pop_dialog(self)
        #self._page.update()

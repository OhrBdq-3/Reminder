import json
import os,sys
import flet as ft


ABOUT = os.path.join(os.getcwd(), 'src','config','about.md')

class About(ft.BottomSheet):
    def __init__(self, page):
        with open(ABOUT, 'r',encoding = 'utf-8') as f:
            about_text = f.read()

        about_container = ft.ListView(
            expand=True,
            spacing=12,
            padding=10,
            controls=[
                ft.Text(
                    "About",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Markdown(
                    about_text,
                ),
            ],
        )
        super().__init__(content = about_container,is_scroll_controlled = True)
        self.page = page
    def open_about(self,):
        print('here')
        self.page.open(self)
        self.page.update()
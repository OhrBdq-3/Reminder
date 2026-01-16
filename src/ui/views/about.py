import os
import sys
import flet as ft

def get_resource_path(relative_path):
    """ 获取资源绝对路径，兼容开发环境和打包后的环境 """
    if hasattr(sys, '_MEIPASS'):
        # 打包后的路径
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)

class About(ft.BottomSheet):
    def __init__(self, page):
        # 这里的路径必须指向 src/config/about.md
        md_path = get_resource_path(os.path.join('src', 'config', 'about.md'))
        
        about_text = "## 关于程序\n未能加载 About.md 内容。"
        
        # 安全读取
        if os.path.exists(md_path):
            try:
                with open(md_path, 'r', encoding='utf-8') as f:
                    about_text = f.read()
            except Exception as e:
                about_text = f"读取 About.md 失败: {e}"
        
        about_container = ft.ListView(
            expand=True,
            spacing=12,
            padding=10,
            controls=[
                ft.Text("About", size=20, weight=ft.FontWeight.BOLD),
                ft.Markdown(about_text),
            ],
        )
        super().__init__(content=about_container, scrollable=True)
        self._page = page

    def open_about(self, e=None):
        self.open=True
        self._page.update()
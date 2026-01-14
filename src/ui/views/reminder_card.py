import flet as ft

class ReminderCard(ft.Card):
    def __init__(self, reminder, on_delete=None, on_edit=None):
        super().__init__()
        self.elevation = 2
        self.reminder = reminder
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.margin = 10

        # 1. 状态判定：是否处于 AI 生成中
        # 这里的判断条件依据 handle_submit 中设置的 "Generating..."
        self.is_generating = "Generating" in self.reminder.title

        # 2. 根据状态配置 UI 元素
        self.setup_status_assets()

        # 3. 创建核心 UI 组件
        self.build_card_components()

        # 4. 组装布局
        self.build_layout()

    def setup_status_assets(self):
        """配置图标、颜色和状态文本"""
        if self.is_generating:
            self.status_color = ft.Colors.BLUE_400
            self.leading_control = ft.Container(
                content=ft.ProgressRing(width=20, height=20, stroke_width=2, color = ft.Colors.AMBER, bgcolor=ft.Colors.BLUE_200),
                padding=5
            )
            self.chip_status = "AI Working"
        else:
            # 正常状态逻辑
            if self.reminder.status == "pending":
                if getattr(self.reminder, 'is_snoozed', 0) == 0:
                    self.status_color = ft.Colors.BLUE_900
                    self.leading_icon = ft.Icons.ALARM
                else:
                    self.status_color = ft.Colors.RED_800
                    self.leading_icon = ft.Icons.SNOOZE_OUTLINED
            elif self.reminder.status == "done":
                self.status_color = ft.Colors.GREEN_900
                self.leading_icon = ft.Icons.AUTO_AWESOME_OUTLINED
            else:
                self.status_color = ft.Colors.RED_900
                self.leading_icon = ft.Icons.DANGEROUS_OUTLINED
            
            self.leading_control = ft.Icon(self.leading_icon, size=30, color=self.status_color)
            self.chip_status = self.reminder.status.capitalize() if getattr(self.reminder, 'is_snoozed', 0) == 0 else "Snoozed"

    def build_card_components(self):
        """构建卡片的各个子控件"""
        # 标题行
        self.up_title = self.reminder.title.title()
        self.pending_hint = ft.Chip(
            label=ft.Text(self.chip_status, width=65, text_align=ft.TextAlign.CENTER, size=11),
            label_style=ft.TextStyle(color=self.status_color, weight=ft.FontWeight.W_700),
            visual_density=ft.VisualDensity.COMPACT,
        )
        
        self.title_row = ft.Row(
            controls=[
                ft.Text(self.up_title or "Just Remind Me", size=18, weight=ft.FontWeight.BOLD, selectable=True, expand=True),
                self.pending_hint
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )

        # 时间显示
        time_str = ""
        try:
            # 处理如果是字符串或 datetime 对象的情况
            t = self.reminder.next_trigger_time if getattr(self.reminder, 'is_snoozed', 0) else self.reminder.base_time
            time_str = t.strftime("%H:%M") if hasattr(t, 'strftime') else str(t)
        except:
            time_str = "--:--"

        prefix = "Snoozed to " if getattr(self.reminder, 'is_snoozed', 0) else ""
        self.time_display = ft.Text(
            f"{self.reminder.option} · {prefix}{time_str}",
            size=13, weight=ft.FontWeight.W_500
        )

        # 描述文本
        self.description_text = ft.Text(
            self.reminder.description, 
            expand=True, 
            selectable=True, 
            size=13, 
            color=ft.Colors.GREY_700
        )

        # 副标题列（动态加入 ProgressBar）
        subtitle_controls = [
            ft.Row([self.time_display], spacing=6),
        ]
        
        if self.is_generating:
            # 插入蓝色进度条增加动态感
            subtitle_controls.append(ft.ProgressBar(height=2, color=ft.Colors.AMBER, bgcolor=ft.Colors.BLUE_300))
            subtitle_controls.append(ft.Text("Parsing your request...", size=12, italic=True, color=ft.Colors.BLUE_700))
        else:
            subtitle_controls.append(self.description_text if self.reminder.description else ft.Text("No description provided"))

        # ListTile 组装
        self.card_content = ft.ListTile(
            leading=self.leading_control,
            title=self.title_row,
            subtitle=ft.Column(controls=subtitle_controls, spacing=4),
            is_three_line=True if self.is_generating else False
        )

        # 按钮操作区
        self.edit_btn = ft.IconButton(
            icon=ft.Icons.EDIT_OUTLINED,
            icon_color=ft.Colors.GREY_600,
            tooltip="Edit",
            disabled=self.is_generating,
            on_click=self.handle_edit
        )

        self.delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color=ft.Colors.GREY_600,
            tooltip="Delete",
            on_click=self.handle_delete
        )

        self.actions = ft.Row(
            controls=[self.edit_btn, self.delete_btn],
            alignment=ft.MainAxisAlignment.END,
            spacing=4,
            opacity=0.0,
            animate_opacity=300,
        )

    def build_layout(self):
        """最终布局组装"""
        self.main_column = ft.Column(
            controls=[
                self.card_content,
                self.actions
            ],
            spacing=0
        )

        self.content = ft.Container(
            content=self.main_column,
            padding=10,
            on_hover=self.on_hover
        )

    def handle_delete(self, e):
        if self.on_delete:
            self.on_delete(self.reminder)

    def handle_edit(self, e):
        if self.on_edit:
            self.on_edit(self.reminder)

    def on_hover(self, e):
        if self.is_generating:
            return
        is_hovered = e.data == "true"
        self.actions.opacity = 1.0 if is_hovered else 0.0
        self.actions.update()
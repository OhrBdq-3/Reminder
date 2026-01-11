import flet as ft
from ui.views.reminder_card import ReminderCard
from ui.views.edit_dialog import EditField
from services.reminder_process import create_reminder
from uuid import uuid4

class CardList(ft.ListView):
    def __init__(self, page: ft.Page, manager):
        super().__init__()
        self.spacing=10
        self.padding=10
        self.auto_scroll=True
        self.expand=True
        
        self.page = page
        self.manager = manager
        
    def reload(self):
        self.controls.clear()
        for d in self.manager.repo.list_all():
            self.controls.append(self._build_card(d))
        self.page.update()
        
    def _build_card(self, reminder):
        return ReminderCard(
            reminder=reminder,
            on_delete=lambda e, r=reminder: self.handle_delete(r),
            on_edit=lambda e, r=reminder: self.open_edit(r),
        )

    def handle_delete(self, reminder):
        self.manager.delete(reminder)
        self.reload()
        self.page.update()
        
    def open_edit(self, old_reminder):
        def handle_submit(title, time, desc, opt):
            self.manager.update(old_reminder, title, time, desc, opt)
            self.reload()          # 👈 刷新在这里
            self.page.update()

        edit_field = EditField(
            old_reminder=old_reminder,
            on_submit=handle_submit
        )

        self.page.overlay.append(edit_field.time_input)
        self.page.open(edit_field)
        self.page.update()
    
    def add_card(self, name, time, description, option):
        new_data = create_reminder(
                id=str(uuid4()),
                title=name,
                base_time=time,
                description=description,
                option=option
            )

        new_card = ReminderCard(
            reminder = new_data,
            on_delete=lambda e, rem = new_data: self.handle_delete(rem),
            on_edit=lambda e, rem = new_data: self.open_edit(rem),
        )
        self.controls.append(new_card)
        #print(new_data)
        self.manager.repo.add(new_data)
        self.page.update()
        
    # def open_edit_dialog(self, old_reminder):
    #     edit_field = EditField(
    #         old_reminder=old_reminder,
    #         on_submit=lambda title, time, desc, opt:
    #             self.update(old_reminder, title, time, desc, opt)
    #     )
    #     self.page.overlay.append(edit_field.time_input)
    #     self.page.open(edit_field)
    #     self.page.update()
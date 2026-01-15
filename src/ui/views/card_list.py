import flet as ft
from ui.views.reminder_card import ReminderCard
from ui.views.edit_dialog import EditField
from services.reminder_process import create_reminder
from uuid import uuid4


DEST_MAP = {
    0:'none',
    1:'pending',
    2:'done'
}

class CardList(ft.ListView):
    def __init__(self, page: ft.Page, manager, sidebar ):
        super().__init__()
        self.spacing=10
        self.padding=10
        self.auto_scroll=True
        self.expand=True
        
        self.page = page
        self.manager = manager
        self.sidebar = sidebar

    def reload(self):
        self.controls.clear()
        for d in self.manager.repo.list_all():
            self.controls.append(self._build_card(d))
        self.page.update()

    def reload_by_status(self, status):
        self.controls.clear()
        for d in self.manager.repo.list_by_status(status):
            self.controls.append(self._build_card(d))
        self.page.update()
        
    def _build_card(self, reminder):
        return ReminderCard(
            reminder=reminder,
            on_delete=lambda e, r=reminder: self.handle_delete(r),
            on_edit=lambda e, r=reminder: self.open_edit(r),
        )

    def handle_delete(self, reminder):
        page_index = self.sidebar.nav.selected_index
        self.manager.delete(reminder)
        if page_index == 0:
            self.reload()
        else:
            self.reload_by_status(DEST_MAP[page_index])
        self.page.update()
        
    def open_edit(self, old_reminder):
        def handle_submit(title, time, desc, opt):
            self.manager.update(old_reminder, title, time, desc, opt)
            page_index = self.sidebar.nav.selected_index
            if page_index == 0:
                self.reload()
            else:
                self.reload_by_status(DEST_MAP[page_index])
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
        self.reload_by_status('pending')
        self.sidebar.nav.selected_index = 1
        self.controls.append(new_card)
        self.manager.repo.add(new_data)
        self.page.update()
        return new_data
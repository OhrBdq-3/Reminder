from services.reminder_process import create_reminder
from ui.views.edit_dialog import EditField

class CardListManager:
    def __init__(self, repo, page, on_refresh = None):
        self.repo = repo
        self.page = page
        self.on_refresh = on_refresh

    def delete(self, reminder):
        self.repo.delete(reminder.id)

    def update(self, reminder, new_title, new_base_time, new_description, new_option):
        reminder.title = new_title
        reminder.base_time = new_base_time
        reminder.description = new_description
        reminder.option = new_option

        updated = create_reminder(
            id=reminder.id,
            title=new_title,
            base_time=new_base_time,
            description=new_description,
            option=new_option
        )

        reminder.next_trigger_time = updated.next_trigger_time
        reminder.base_time = updated.base_time
        reminder.repeat = updated.repeat
        reminder.status = "pending"
        self.repo.update(reminder)
        #return updated
        
    # def open_edit_dialog(self, old_reminder):
    #     edit_field = EditField(
    #         old_reminder=old_reminder,
    #         on_submit=lambda title, time, desc, opt:
    #             self.update(old_reminder, title, time, desc, opt)
    #     )
    #     self.page.overlay.append(edit_field.time_input)
    #     self.page.open(edit_field)
    #     self.page.update()
import flet as ft
from services.mail_reminder_service import convert_mails_to_reminder
from engine.model_engine import ChatEngine
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

pull_executor = ThreadPoolExecutor(max_workers=2)

class PullMailBtn(ft.TextButton):
    def __init__(self, page, on_submit = None, on_update = None):
        super().__init__()
        self.on_submit = on_submit
        self.on_update = on_update
        self._page = page
        self.content = "Pull Mail"
        self.icon = ft.Icons.MAIL_OUTLINE
        self.on_click = self.handle_click
        self.engine = ChatEngine()
        self.running = False

        
    def handle_click(self, e):
        if self.running:
            print('clicked again')
            return
        self.running = True
        self.loading = self.on_submit(
            name="Pulling mails & Generating...",
            time=datetime.now().time().strftime("%H:%M:%S"),
            description="AI is working",
            option="Tomorrow"
        )

        future = pull_executor.submit(
            convert_mails_to_reminder,
            self.engine
        )

        future.add_done_callback(
            lambda f: self._page.run_thread(
                self._on_task_done,
                f.result()
            )
        )
        
    def _on_task_done(self, results):
        self.running = False

        if not results:
            self.on_update(
                self.loading,
                "No new mails / Failed",
                datetime.now().strftime("%H:%M:%S"),
                "IMAP timeout or no new mails",
                "Today"
            )
            self.running = False
            self._page.update()
            return

        self._render_cards_from_results(results)
    
    def _render_cards_from_results(self, results):
        if results is not None:
            
            if self.loading:
                result = results[0]
                self.on_update(
                    self.loading,
                    result.get("title", ""),
                    result.get("datetime", ""),
                    result.get("description", ""),
                    result.get("option", ""),
                )
                self._page.update()

            for result in results[1:]:
                card = self.on_submit(
                    name=result.get("title", "Mail"),
                    time=result.get("datetime", ""),
                    description=result.get("description", ""),
                    option=result.get("option", ""),
                )

                if self.on_update:
                    self.on_update(
                        card,
                        result.get("title", ""),
                        result.get("datetime", ""),
                        result.get("description", ""),
                        result.get("option", ""),
                    )
        self.running = False
        self._page.update()
        
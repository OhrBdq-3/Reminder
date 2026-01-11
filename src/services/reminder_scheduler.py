import threading
import time
from datetime import datetime, timedelta
from services.reminder_repo import ReminderRepository

class ReminderScheduler:
    def __init__(self, repo, on_trigger):
        self.repo = repo
        self.on_trigger = on_trigger
        self.running = False
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(
            target = self._run,
            daemon = True
        )
        self.thread.start()
    
    def stop(self):
        self.running = False

    def _run(self):
        triggered = set()
        while self.running:
            print(self.repo.list_all())
            print(f'triggered set:{triggered}')
            now = datetime.now()
            today = now.date()
            for r in self.repo.list_all():
                key = (r.id, r.next_trigger_time)
                repeat = r.repeat
                status = r.status
                next_trigger_time = r.next_trigger_time

                if repeat == "none" and status == "pending":
                    if next_trigger_time <= now and key not in triggered:
                        triggered.add(key)
                        self.on_trigger(r)
                        #self._after_triggered(r)
                        print('triggered none')

                elif repeat == "daily" and status == "pending":
                    if next_trigger_time <= now and key not in triggered:
                        triggered.add(key)
                        self.on_trigger(r)
                        #self._after_triggered(r)
                        print('triggered daily')

                elif repeat == "workdays" and status == "pending":
                    if now.weekday() not in [5,6]:
                        if next_trigger_time <= now and key not in triggered:
                            triggered.add(key)
                            self.on_trigger(r)
                            #self._after_triggered(r)
                            print('triggered workdays')

                elif repeat == "weekend" and status == "pending":
                    if now.weekday() in [5,6]:
                        if next_trigger_time <= now and key not in triggered:
                            triggered.add(key)
                            self.on_trigger(r)
                            #self._after_triggered(r)
                            print('triggered weekend')
            time.sleep(30)

    def _after_triggered(self,r):
        if r.repeat == "none":
            r.status = "done"

        elif r.repeat == "daily":
            r.next_trigger_time += timedelta(days=1)
        
        elif r.repeat == "workdays":
            d = r.next_trigger_time
            while True:
                d += timedelta(days = 1)
                if d.weekday() < 5:
                    break
            r.next_trigger_time = d
        
        elif r.repeat == "weekend":
            d = r.next_trigger_time
            while True:
                d += timedelta(days = 1)
                if d.weekday() >= 5:
                    break
            r.next_trigger_time = d
        self.repo.update(r)
import time
from tkinter import Label

class Timer:
    def __init__(self, label):
        self.label = label
        self.start_time = None
        self.timer_id = None

    def start(self):
        # Calculates the start time and sends for an update
        self.start_time = time.time()
        self.update()

    def update(self):
        # Calculate the time that has passed
        time_elapsed = time.time() - self.start_time
        self.label.configure(text=f"{time_elapsed:.1f}")
        self.timer_id = self.label.after(1, self.update)

    def stop(self):
        if self.timer_id is not None:
            self.label.after_cancel(self.timer_id)
            self.timer_id = None

# main.py
from indicators.analysis_wrapper import AnalysisEngine
import tkinter as tk
from interface.event_handlers import EventHandlers
from indicators.signal_generator import generate_signals
from data.tv_master import TvDataFeedMaster
import config
from threading import Thread
import time
from config import Settings

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Signal Analyzer")
        self.settings = Settings()
        self.tv = TvDataFeedMaster()
        
        # Передаём функцию generate_signals напрямую
        self.engine = AnalysisEngine(self.tv)
        self.gui = EventHandlers(self.root, self.engine)  

        self.auto_update()

    def auto_update(self):
        def loop():
            while True:
                print("Обновление графика и сигналов...")
                self.gui.handle_auto_update()
                time.sleep(60)

        t = Thread(target=loop, daemon=True)
        t.start()

if __name__ == "__main__":
    print("Приложение запускается...")
    root = tk.Tk()
    app = App(root)
    root.mainloop()
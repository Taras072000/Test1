class EventHandlers:
    def __init__(self, main_window, analysis_engine):
        self.main_window = main_window
        self.analysis_engine = analysis_engine

        # Назначаем обработчики событий
        self.main_window.run_button.config(command=self.handle_run_clicked)
        self.main_window.pair_selector.bind("<<ListboxSelect>>", self.handle_pair_changed)

        # Таймер будет использовать after() в tkinter
        self.start_auto_update()

    def handle_run_clicked(self):
        selected_index = self.main_window.pair_selector.curselection()
        if not selected_index:
            return
        pair = self.main_window.pair_selector.get(selected_index[0])
        self.append_log(f"Запуск анализа для {pair}")

        signals = self.analysis_engine.run_analysis(pair)
        self.display_signals(signals)

    def handle_pair_changed(self, event):
        selected_index = self.main_window.pair_selector.curselection()
        if not selected_index:
            return
        pair = self.main_window.pair_selector.get(selected_index[0])
        self.append_log(f"Выбрана новая пара: {pair}")

    def display_signals(self, signals):
        if not signals:
            self.append_log("Сигналов нет.")
            return

        for signal in signals:
            self.append_log(f"[{signal['type'].upper()}] {signal['message']}")

    def append_log(self, message):
        self.main_window.log_output.insert(tk.END, message + "\n")
        self.main_window.log_output.see(tk.END)

    def start_auto_update(self):
        self.handle_auto_update()
        self.main_window.root.after(60000, self.start_auto_update)  # 60 сек

    def handle_auto_update(self):
        selected_index = self.main_window.pair_selector.curselection()
        if not selected_index:
            return
        pair = self.main_window.pair_selector.get(selected_index[0])
        self.append_log(f"Автообновление анализа для {pair}")
        signals = self.analysis_engine.run_analysis(pair)
        self.display_signals(signals)
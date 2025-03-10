import tkinter as tk
import threading

class GUIManager:
    def __init__(self, app):
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        """Tworzy wszystkie elementy GUI."""
        self.entry_label = tk.Label(self.app, text="Wpisz coś:")
        self.entry_label.grid(row=0, column=0, padx=10, pady=5)

        self.entry = tk.Entry(self.app)
        self.entry.grid(row=0, column=1, padx=10, pady=5)

        self.checkbox_pos_var = tk.BooleanVar()
        self.checkbox_pos = tk.Checkbutton(self.app, text="Pozycja:", variable=self.checkbox_pos_var,
                                           command=lambda: self.app.task_manager.toggle_task("pos", 300))
        self.checkbox_pos.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        self.text_display = tk.Text(self.app, height=1, width=15, state='disabled')
        self.text_display.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

        self.button = tk.Button(self.app, text="TEST", command=self.app.on_e_press)
        self.button.grid(row=10, column=0, columnspan=2, padx=10, pady=5)
        # ---------------------------
        #
        # # Check box- Auto atak
        # self.checkbox_attack_var = tk.BooleanVar()
        # self.checkbox_attack = tk.Checkbutton(self, text="Auto atak:", variable=self.checkbox_attack_var,
        #                                       command=self.toggle_attack_checkbox)
        # self.checkbox_attack.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)
        # #
        # # # Check box- Auto chodzenia
        # self.checkbox_walk_var = tk.BooleanVar()
        # self.checkbox_walk = tk.Checkbutton(self, text="Auto chodzenie:", variable=self.checkbox_walk_var,
        #                                       command=self.toggle_walk_checkbox)
        # self.checkbox_walk.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)
        # #
        # Check box- Auto key 4
        self.checkbox_key_f1_var = tk.BooleanVar()
        self.checkbox_key_f1 = tk.Checkbutton(self.app, text="key f1:", variable=self.checkbox_key_f1_var,
                                            command=lambda: self.app.task_manager.toggle_task("key_f1", 200))
        self.checkbox_key_f1.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Check box- Auto pickup
        self.checkbox_key_z_var = tk.BooleanVar()
        self.checkbox_key_z = tk.Checkbutton(self.app, text="auto pickup:", variable=self.checkbox_key_z_var,
                                           command=lambda: self.app.task_manager.toggle_task("key_z", 200))
        self.checkbox_key_z.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Check box - Auto Key
        self.checkbox_key_var = tk.BooleanVar()
        self.checkbox_key = tk.Checkbutton(self.app, text="auto key:", variable=self.checkbox_key_var,
                                             command=lambda: self.app.task_manager.toggle_task("key", self.convert_to_int(self.entry_key_time.get())))
        self.checkbox_key.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        self.entry_key = tk.Entry(self.app)
        self.entry_key.grid(row=6, column=1, padx=10, pady=5)

        self.entry_key_time = tk.Entry(self.app)
        self.entry_key_time.grid(row=6, column=2, padx=10, pady=5)
        #
        # # Check box - Chane direction
        # self.checkbox_change_direction_var = tk.BooleanVar()
        # self.checkbox_change_direction= tk.Checkbutton(self, text="auto zmiana kierunku:", variable=self.checkbox_change_direction_var,
        #                                    command=self.toggle_change_direction_checkbox)
        # self.checkbox_change_direction.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)
        #
        # # # Lista rozwijana
        # # self.combobox_label = tk.Label(self, text="Wybierz opcję:")
        # # self.combobox_label.grid(row=5, column=0, padx=10, pady=5)
        # #
        # # self.combobox = ttk.Combobox(self, values=["Opcja 1", "Opcja 2", "Opcja 3"])
        # # self.combobox.grid(row=5, column=1, padx=10, pady=5)
        # #
        #
        # # Check box - Auto Key
        # self.checkbox_script_var = tk.BooleanVar()
        # self.checkbox_script = tk.Checkbutton(self, text="script_loop:", variable=self.checkbox_script_var,
        #                                      command=self.toggle_script_checkbox)
        # self.checkbox_script.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)
        #
        # self.entry_script = tk.Entry(self)
        # self.entry_script.grid(row=8, column=1, padx=10, pady=5)
        #
        # #  ------------------------------------------------------  -----------------------------------------------------
        # self.checkbox_color_var = tk.BooleanVar()
        # self.checkbox_color = tk.Checkbutton(self, text="press_if_color:", variable=self.checkbox_color_var,
        #                                      command=self.toggle_color_checkbox)
        # self.checkbox_color.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)
        #
        # self.entry_color = tk.Entry(self)
        # self.entry_color.grid(row=9, column=1, padx=10, pady=5)
        #
        # # Pole tekstowe tylko do odczytu
        # self.text_color_display = tk.Text(self, height=1, width=15, state='disabled')
        # self.text_color_display.grid(row=9, column=2, columnspan=2, padx=10, pady=5)
        # self.update_text(self.text_color_display, "F12-getCol")
        #
        # self.text_color_rgb_display = tk.Text(self, height=1, width=15, state='disabled')
        # self.text_color_rgb_display.grid(row=9, column=3, columnspan=2, padx=10, pady=5)
        # ---------------------------

        self.text_color_rgb_display = tk.Text(self.app, height=1, width=15, state='disabled')
        self.text_color_rgb_display.grid(row=9, column=3, columnspan=2, padx=10, pady=5)

        # #  ------------------------------------------------------  -----------------------------------------------------
        self.checkbox_fishing_var = tk.BooleanVar()
        self.checkbox_fishing = tk.Checkbutton(self.app, text="fish bot:", variable=self.checkbox_fishing_var,
                                             command=self.toggle_fishing)
        self.checkbox_fishing.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

    def toggle_fishing(self):
        if self.checkbox_fishing_var.get():
            # Uruchom wędkowanie w osobnym wątku
            fishing_thread = threading.Thread(target=self.app.fishing_bot.start_fishing, daemon=True)
            fishing_thread.start()
        else:
            self.app.fishing_bot.stop_fishing()

    def update_text(self, text_widget, message):
        """Aktualizuje zawartość pola tekstowego."""
        text_widget.config(state='normal')
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, message)
        text_widget.config(state='disabled')

    def convert_to_int(self, str):
        try:
            return int(str)
        except ValueError:
            print("Nie można przekonwertować na liczbę całkowitą.")
            return -1

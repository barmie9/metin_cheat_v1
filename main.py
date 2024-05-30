import time
import tkinter as tk
from tkinter import ttk
from pynput import keyboard # Do globalnego przechwytywania klawitury np F12
from memory_service import MemoryService
from script_service import ScriptService


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Przykładowa aplikacja Tkinter")

        # Tworzenie i rozmieszczanie widżetów
        self.create_widgets()

        # Uruchomienie globalnego listenera dla klawiatury
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

        # Tworzenie serwisu dla pamięci procesu
        self.memory_service = MemoryService()

        # Id metod powtarzanych w pętli
        # self.after_id_key_z = None
        self.after_ids = {}  # Dictionary to store after_id for each task

        self.script_service = ScriptService()



    def create_widgets(self):
        # Pole input
        self.entry_label = tk.Label(self, text="Wpisz coś:")
        self.entry_label.grid(row=0, column=0, padx=10, pady=5)

        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=1, padx=10, pady=5)

        # Check box - Wyświetlanie pozycji
        self.checkbox_pos_var = tk.BooleanVar()
        self.checkbox_pos = tk.Checkbutton(self, text="Pozycja:", variable=self.checkbox_pos_var, command=self.toggle_pos_checkbox)
        self.checkbox_pos.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)
        #
        # Pole tekstowe tylko do odczytu
        self.text_display = tk.Text(self, height=1, width=15, state='disabled')
        self.text_display.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
        #
        # Check box- Auto atak
        self.checkbox_attack_var = tk.BooleanVar()
        self.checkbox_attack = tk.Checkbutton(self, text="Auto atak:", variable=self.checkbox_attack_var,
                                              command=self.toggle_attack_checkbox)
        self.checkbox_attack.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)
        #
        # # Check box- Auto chodzenia
        self.checkbox_walk_var = tk.BooleanVar()
        self.checkbox_walk = tk.Checkbutton(self, text="Auto chodzenie:", variable=self.checkbox_walk_var,
                                              command=self.toggle_walk_checkbox)
        self.checkbox_walk.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)
        #
        # Check box- Auto key 4
        self.checkbox_key_f1_var = tk.BooleanVar()
        self.checkbox_key_f1 = tk.Checkbutton(self, text="key f1:", variable=self.checkbox_key_f1_var,
                                            command=self.toggle_key_f1_checkbox)
        self.checkbox_key_f1.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Check box- Auto chodzenia
        self.checkbox_key_z_var = tk.BooleanVar()
        self.checkbox_key_z = tk.Checkbutton(self, text="auto pickup:", variable=self.checkbox_key_z_var,
                                           command=self.toggle_key_z_checkbox)
        self.checkbox_key_z.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Check box - Auto Key
        self.checkbox_key_var = tk.BooleanVar()
        self.checkbox_key = tk.Checkbutton(self, text="auto key:", variable=self.checkbox_key_var,
                                             command=self.toggle_key_checkbox)
        self.checkbox_key.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        self.entry_key = tk.Entry(self)
        self.entry_key.grid(row=6, column=1, padx=10, pady=5)

        # Check box - Chane direction
        self.checkbox_change_direction_var = tk.BooleanVar()
        self.checkbox_change_direction= tk.Checkbutton(self, text="auto zmiana kierunku:", variable=self.checkbox_change_direction_var,
                                           command=self.toggle_change_direction_checkbox)
        self.checkbox_change_direction.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # # Lista rozwijana
        # self.combobox_label = tk.Label(self, text="Wybierz opcję:")
        # self.combobox_label.grid(row=5, column=0, padx=10, pady=5)
        #
        # self.combobox = ttk.Combobox(self, values=["Opcja 1", "Opcja 2", "Opcja 3"])
        # self.combobox.grid(row=5, column=1, padx=10, pady=5)
        #

        # Check box - Auto Key
        self.checkbox_script_var = tk.BooleanVar()
        self.checkbox_script = tk.Checkbutton(self, text="script_loop:", variable=self.checkbox_script_var,
                                             command=self.toggle_script_checkbox)
        self.checkbox_script.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        self.entry_script = tk.Entry(self)
        self.entry_script.grid(row=8, column=1, padx=10, pady=5)

        # Przycisk
        self.button = tk.Button(self, text="TEST", command=self.on_button_click)
        self.button.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

        self.is_key_pressed = False
        self.is_key_z_pressed = False



    def on_button_click(self):
        # # Pobieranie wartości z widżetów
        #         # entry_value = self.entry.get()
        #         # checkbox_value = self.checkbox_var.get()
        #         # combobox_value = self.combobox.get()
        #         #
        #         # # Wyświetlanie wartości w konsoli
        #         # print(f"Pole input: {entry_value}")
        #         # print(f"Checkbox: {'zaznaczony' if checkbox_value else 'niezaznaczony'}")
        #         # print(f"Lista rozwijana: {combobox_value}")
        time.sleep(1)
        self.memory_service.horse_key_execute()

    def update_pos_text(self):
        message = self.memory_service.get_coordinate()
        self.text_display.config(state='normal')  # Odblokowanie pola tekstowego
        self.text_display.delete(1.0, tk.END)  # Usunięcie istniejącej zawartości
        self.text_display.insert(tk.END, message)  # Wstawienie nowej zawartości
        self.text_display.config(state='disabled')  # Ponowne zablokowanie pola tekstowego

    def toggle_pos_checkbox(self):
        self.toggle_task('pos', self.update_pos_text, 300)



    def toggle_attack_checkbox(self):
        self.memory_service.inject_test()
        # if self.checkbox_attack_var.get():
        #     self.memory_service.attack(True)
        # else:
        #     self.memory_service.attack(False)


    def toggle_walk_checkbox(self):
        self.toggle_task('walk', self.memory_service.walk_to_point, 100, (57500, 64200))

    def toggle_key_z_checkbox(self):
        self.toggle_task('key_z', self.memory_service.click_key, 200, 'z', 0.02)

    def toggle_key_checkbox(self):
        self.toggle_task('key', self.memory_service.click_key, 200, self.entry_key.get(), 0.02)

    def toggle_script_checkbox(self):
        self.toggle_task('script', self.script_service.execute_script, 100, self.entry_script.get(), self.checkbox_script_var.get())

    def toggle_key_f1_checkbox(self):
        self.toggle_task('key_f1', self.memory_service.click_key, 600, 'F1', 0.02)

    def toggle_change_direction_checkbox(self):
        self.toggle_task('change_direction', self.memory_service.change_direction, 20000)

    def toggle_task(self, task_name, method, time_ms, *args):
        if getattr(self, f'checkbox_{task_name}_var').get():
            self.after_ids[task_name] = self.method_repeater(task_name, method, time_ms, *args)
            print(f"{task_name} after_id: {self.after_ids[task_name]}")
        elif task_name in self.after_ids:
            print(f"Anulowanie funkcji {task_name}: {self.after_ids[task_name]}")
            self.after_cancel(self.after_ids[task_name])
            self.after_ids[task_name] = None

    def method_repeater(self, task_name, method, time_ms, *args):
        print(f"method_repeater: {task_name} after_id: {self.after_ids.get(task_name)}")
        method(*args)
        self.after_ids[task_name] = self.after(time_ms, self.method_repeater, task_name, method, time_ms, *args)
        return self.after_ids[task_name]

    def on_key_press(self, key):
        # Funkcja reagująca na wciśnięcie klawisza F12
        try:
            if key == keyboard.Key.f12:
                self.on_f12_press()
        except AttributeError:
            pass

    def on_f12_press(self):
        # Działania do wykonania po naciśnięciu klawisza F12
        print("Klawisz F12 został wciśnięty (globalnie)")
        # Można dodać tutaj dalsze operacje

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

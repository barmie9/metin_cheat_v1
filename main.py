import time
import tkinter as tk
from pynput import keyboard

from gui_manager import GUIManager
from lowienie_metin2009 import LowienieMetin
from task_manager import TaskManager
from config_metin import MetinConfig
from memory_service import MemoryService
from script_service import ScriptService
from capture_dxcam import CaptureDxcam


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Metin2 Cheat")
        self.config = MetinConfig('config.cfg')

        # Inicjalizacja usług
        self.memory_service = MemoryService(self.config)
        self.script_service = ScriptService(self.config)
        # self.capture_service = CaptureDxcam()
        self.fishing_bot = LowienieMetin(self)


        # Zarządzanie GUI
        self.gui_manager = GUIManager(self)

        # Zarządzanie zadaniami
        self.task_manager = TaskManager(self)

        # Uruchomienie globalnego nasłuchiwania klawiatury
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def on_key_press(self, key):
        """Obsługuje globalne skróty klawiaturowe."""
        try:
            if key == keyboard.Key.f12:
                self.on_f12_press()
            elif key == keyboard.Key.f11:
                self.on_f11_press()
            elif key.char.lower() == 'e':
                self.on_e_press()
        except Exception as e:
            print(f"Błąd obsługi klawisza: {e}")

    def on_f12_press(self):
        """Aktualizuje kolor po naciśnięciu F12."""
        print("F12 - Aktualizacja koloru")
        color = self.memory_service.update_color()
        self.gui_manager.update_text(self.gui_manager.text_color_rgb_display, color)

    def on_f11_press(self):
        """Wykonuje zrzut ekranu po naciśnięciu F11."""
        print("F11 - Screenshot")
        self.capture_service.capture_screen()

    def on_e_press(self):
        """Akcja przypisana do klawisza E."""
        print("E - Wykonanie horse_key_execute()")
        self.memory_service.horse_key_execute()


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

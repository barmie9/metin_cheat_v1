import os
import time
import mss
import ctypes
import random
import pygame

from datetime import datetime
from capture_dxcam import CaptureDxcam
from memory_service import MemoryService


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class LowienieMetin:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.memory_service = MemoryService()
        self.capture_dxcam = CaptureDxcam()
        self.capture_dxcam.screenshot()  # Pierwsze wywolanie wywala bleda, dlatego robie je tutaj, musi wykonac sie w grze metin

    def key_space(self):
        self.memory_service.click_key_not_thread("space", 0.07)
        # self.memory_service.click_key("space", 0.02)

    def key_f1(self):
        self.memory_service.click_key_not_thread("F1", 0.07)
        # self.memory_service.click_key("F1", 0.03)

    def screenshot(self):
        self.capture_dxcam.screenshot()

    def get_pixel_color_from_point(self, x, y):
        color = self.capture_dxcam.get_pixel_from_screenshot(x, y)
        # print("PIXEL: ", x, "x", y, " - > ", color)
        if color[0] == -1 or color[1] == -1 or color[2] == -1:
            self.log_fishing("ERROR", "Blad pobrania koloru dla pixel: " + str(x) + "x" + str(y) )
        return color
        # with mss.mss() as sct:
        #     monitor = {"top": y, "left": x, "width": 1, "height": 1}
        #     screenshot = sct.grab(monitor)
        #     pixel = tuple(map(int, screenshot.pixel(0, 0)))  # Konwersja na int
        #     return pixel[:3]  # RGB

    def is_fish(self):
        # r, g, b = self.get_pixel_color_from_point(1048, 163)
        r, g, b = self.get_pixel_color_from_point(420, 40)
        return r > 235 and g > 235 and b > 235

    def is_game_on(self):
        # r, g, b = self.get_pixel_color_from_point(776, 683)
        # r, g, b = self.get_pixel_color_from_point(325, 444)
        x = 300
        y = 446
        r, g, b = self.capture_dxcam.get_pixel_from_screenshot(x, y)
        if r == -1:
            self.log_fishing("ERROR", "Blad pobrania koloru dla pixel: " + str(x) + "x" + str(y))
            return False
        # return r < 63 and g > 80 and g < 112 and b < 57
        self.log_fishing("WAR", "KOLOR is_game_on: "+str(r)+","+str(g)+","+str(b)+" , XY: " + str(x) + "x" + str(y))
        return r == 116 and g == 103 and b == 76

    def fishing_game(self):
        with mss.mss() as sct:
            # Making screenshot:
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            screenshot = sct.grab(monitor)

            # Checking pixels:
            # R&G&B < 65 = black
            # R&G&B > 170 = fish
            # R|G|B > 69 & R&G&B < 170
            # 776x396 - 776x683
            x = 776

            # y cord:
            bottom_mov = 0
            top_mov = 0
            fish_mov = 0
            # Checking pixels from bottom to top:
            for i in range(683, 395, -1):
                # print(i)
                pixel = tuple(map(int, screenshot.pixel(x, i)))  # Konwersja na int
                # print(pixel[:3])
                pix_res = self.check_pixel(pixel[:3])
                if fish_mov == 0 and pix_res == 1:
                    fish_mov = i
                    # print("RYBA " + str(i))
                if bottom_mov == 0 and pix_res == 2:
                    bottom_mov = i
                    # print("DOL " + str(i))
                if top_mov == 0 and bottom_mov != 0 and fish_mov != 0 and pix_res == 0 and abs(fish_mov - i) > 8:
                    top_mov = i
                    # print("GORA " + str(i))
                if top_mov == 0 and i == 396:
                    top_mov = i
                    self.log_fishing("INFO", "Wykryto kolorowy pasek na samej gorze")

            if (bottom_mov - (bottom_mov - top_mov) / 2) < fish_mov:
                self.log_fishing("INFO", "GAME: press space")
                self.key_space()

            if top_mov == 396:
                return False
            else:
                return True

    def fishing_game_v2(self):
        # Making screenshot:
        self.capture_dxcam.screenshot()
        time.sleep(0.19)

        # Checking pixels:
        # R&G&B < 65 = black
        # R&G&B > 170 = fish
        # R|G|B > 69 & R&G&B < 170
        # 325x444 - 325x155
        x = 325

        # y cord:
        bottom_mov = 0
        top_mov = 0
        fish_mov = 0
        # Checking pixels from bottom to top:
        for i in range(444, 154, -1):
            # print(i)
            pixel = self.capture_dxcam.get_pixel_from_screenshot(x, i)  # tuple(map(int, screenshot.pixel(x, i)))  # Konwersja na int
            if pixel[0] == -1:
                # print("ERROR: PIXEL: ", pixel)
                self.log_fishing("ERROR", "(game) Blad pobrania koloru dla pixel: " + str(x) + "x" + str(i) )
                return
            # print(pixel[:3])
            pix_res = self.check_pixel(pixel[:3])
            if fish_mov == 0 and pix_res == 1:
                fish_mov = i
                # print("RYBA " + str(i))
            if bottom_mov == 0 and pix_res == 2:
                bottom_mov = i
                # print("DOL " + str(i))
            if top_mov == 0 and bottom_mov != 0 and fish_mov != 0 and pix_res == 0 and abs(fish_mov - i) > 8:
                top_mov = i
                # print("GORA " + str(i))
            if top_mov == 0 and i == 155:
                top_mov = i
                self.log_fishing("INFO", "Wykryto kolorowy pasek na samej gorze")

        if (bottom_mov - (bottom_mov - top_mov) / 2) < (fish_mov + 9):
            self.log_fishing("INFO", "GAME: press space")
            # SPACJA
            self.key_space()

        if top_mov == 155:
            return False
        else:
            return True

            # for i in range(683, 395, -1):
            #
            #     pixel = tuple(map(int, screenshot.pixel(x, i)))  # Konwersja na int
            #     print(pixel[:3])

    # 0 - blank, 1 - fish, 2 - moving field, 3 - error
    def check_pixel(self, pixel):
        r, g, b = pixel
        if r < 65 and g < 65 and b < 65:
            return 0
        if r > 170 and g > 170 and b > 170:
            return 1
        if (r > 69 or g > 69 or b > 69) and (r < 170 and g < 170 and b < 170):
            return 2
        else:
            return 3

    def save_screen_shot(self):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join("screenshots", f"screenshot_{timestamp}.png")

        with mss.mss() as sct:
            # Przechwytuje cały ekran (wszystkie monitory)
            screenshot = sct.grab(sct.monitors[1])  # monitors[0] to cały obszar ekranu
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_path)

        print(f"Zrzut ekranu zapisany jako {screenshot_path}")

    def rand_num(self, min: float, max: float) -> float:
        return random.uniform(min, max)

    def alarm(self, rep_num: int):
        pygame.mixer.init()
        for _ in range(rep_num):
            pygame.mixer.music.load("alarm_01.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # Czekaj na zakończenie odtwarzania
                time.sleep(0.1)

    def is_messaging(self):
        # r, g, b = self.get_pixel_color_from_point(1867, 330)
        r, g, b = self.get_pixel_color_from_point(745, 192)
        # RGB dla wiad od sklepu: 233,223,245
        return r > 245 and g > 245 and b > 245 # Rozny kolor dla wiad od sklepu i dla wiad od gracza, a gm?

    def log_fishing(self, type, message):
        # Pobierz aktualny czas
        current_time = datetime.now()

        # Sformatuj czas jako godzina:minuta:sekunda:milisekunda
        formatted_time = current_time.strftime("%H:%M:%S:%f")[:-3]  # Usuń ostatnie 3 cyfry mikrosekund

        # Wydrukuj log
        print(f"[{type}] - ({formatted_time}) -> {message}")


time.sleep(5)
fishing = LowienieMetin()
# F1
fishing.key_f1()
time.sleep(0.2)
# SPACJA
fishing.key_space()
prev_fish_time = time.time()
while True:
    fishing.screenshot()

    # Jesli przez 44s nie pojawi sie dymek to zarzuc jeszcze raz:
    if (time.time() - prev_fish_time) > 44:
        fishing.log_fishing("WAR", "44 sek bez przyn. Ponowne zarzucenie...")
        fishing.key_f1()
        time.sleep(0.3)
        fishing.key_space()
        prev_fish_time = time.time()

    if fishing.is_fish():
        fishing.log_fishing("INFO", "Bierze !  !!")
        prev_fish_time = time.time()
        # time.sleep(2.5) #od 1.8 do 2.5s
        time.sleep(fishing.rand_num(1.5, 2.3))
        fishing.log_fishing("INFO", "Szarpniecie wedki")
        # SPACJA
        fishing.key_space()
        is_game = False
        for i in range(14):  # TODO Mozliwe ze trzeba zmienic na 3 sekundy 0.2*x=3s, nie zazuca jesli nieudana proba
            fishing.screenshot()
            time.sleep(0.2)
            if fishing.is_game_on():
                fishing.log_fishing("INFO", "Wykryto gre")
                is_game = True
                break

        if is_game:
            fishing.log_fishing("INFO", "Rozpoczynamy gre")
            start_time = time.time() # Gra trwa okolo od 10 do 15 sekund
            while fishing.fishing_game_v2():
                # time.sleep(0.01)
                if (time.time() - start_time) > 19.5:
                    fishing.log_fishing("WAR", "Gra nieudana minelo 20 sekund")
                    break
            # time.sleep(3) #2.9 3.4
            fishing.log_fishing("INFO", "Gra skonczona")
            time.sleep(fishing.rand_num(4.2, 4.5))
        else:
            fishing.log_fishing("INFO", "Brak ryby na haczyku")
            time.sleep(fishing.rand_num(1.0, 1.7))
        # F1
        fishing.key_f1()
        time.sleep(0.3)
        # SPACJA
        fishing.log_fishing("INFO", "Zarzucenie wedki")
        fishing.key_space()

    # fishing.fishing_game()
    fishing.log_fishing("INFO", "------------ czy bierze ------------")
    time.sleep(0.3)
    if fishing.is_messaging():
        fishing.log_fishing("INFO", "WYKRYTO WIADOMOSC!")
        fishing.alarm(3)

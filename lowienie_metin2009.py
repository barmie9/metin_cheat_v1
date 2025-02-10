import os
import time
import mss
import ctypes

from openpyxl.chart.data_source import NumData

from memory_service import MemoryService


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class LowienieMetin:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.memory_service = MemoryService()

    def key_space(self):
        self.memory_service.click_key("space", 0.02)

    def key_f1(self):
        self.memory_service.click_key("F1", 0.02)

    def get_pixel_color_from_point(self, x, y):
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": 1, "height": 1}
            screenshot = sct.grab(monitor)
            pixel = tuple(map(int, screenshot.pixel(0, 0)))  # Konwersja na int
            return pixel[:3]  # RGB

    def is_fish(self):
        r, g, b = self.get_pixel_color_from_point(1048, 163)
        return r > 240 and g > 240 and b > 240

    def is_game_on(self):
        r, g, b = self.get_pixel_color_from_point(776, 683)
        print("RGB: ", r,g,b)
        return r < 103 and g > 90 and g < 115 and b < 95

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
                    print("RYBA " + str(i))
                if bottom_mov == 0 and pix_res == 2:
                    bottom_mov = i
                    print("DOL " + str(i))
                if top_mov == 0 and bottom_mov != 0 and fish_mov != 0 and pix_res == 0 and abs(fish_mov - i) > 8:
                    top_mov = i
                    print("GORA " + str(i))
                if top_mov == 0 and i == 396:
                    top_mov = i
                    print("GORA " + str(i))

            if (bottom_mov - (bottom_mov - top_mov)/2) < fish_mov:
                print("JUMP")
                # SPACJA
                self.key_space()

            if top_mov == 396:
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

# fishing = LowienieMetin()
#
# # fishing.fishing_game()
#
# time.sleep(5)
# # F1
# fishing.key_f1()
# time.sleep(0.2)
# # SPACJA
# fishing.key_space()
# while True:
#     if fishing.is_fish():
#         print(" Bierze !  !!")
#         time.sleep(2.5) #od 2 do 3s
#         print("Bomba ")
#         # SPACJA
#         fishing.key_space()
#         is_game = False
#         for i in range(22):
#             if fishing.is_game_on():
#                 print("GAME ON ")
#                 is_game = True
#                 break
#             time.sleep(0.2)
#         if is_game:
#             while fishing.fishing_game():
#                 print("FISHING GAME RUNNING! ")
#                 time.sleep(0.2)
#         # F1
#         fishing.key_f1()
#         time.sleep(0.2)
#         # SPACJA
#         fishing.key_space()
#
#     # fishing.fishing_game()
#     print("------------------")
#     time.sleep(0.2)


# while True:
#     print("                   ", fishing.is_game_on())
#     time.sleep(0.5)

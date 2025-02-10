import time
import mss
import ctypes

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class ColorService:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 0, 0)

    def get_pixel_color_from_point(self, x, y):
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": 1, "height": 1}
            screenshot = sct.grab(monitor)
            pixel = tuple(map(int, screenshot.pixel(0, 0)))  # Konwersja na int
            return pixel[:3]  # RGB

    def get_pixel_color(self):
        return self.get_pixel_color_from_point(self.x, self.y)

    def set_point(self, x, y):
        self.x = x
        self.y = y

    def update_color(self):
        self.color = self.get_pixel_color()
        return self.color

    def get_mouse_position(self):
        pt = POINT()  # Używamy własnej struktury POINT
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y

    def is_color_equal(self, color):
        return self.color[0] == color[0] and self.color[1] == color[1] and self.color[2] == color[2]


# col_ser = ColorService(100, 100)
# for i in range(30):
#     time.sleep(2)
#     x, y = col_ser.get_mouse_position()
#     print(col_ser.get_pixel_color_from_point(x, y))

import dxcam
import time
import cv2

class CaptureDxcam:

    def __init__(self):
        # self.camera = dxcam.create(output_color="BGR")  # Kompatybilne z OpenCV
        self.camera = dxcam.create()
        self.frame = self.camera.grab()
        # self.camera = dxcam.create()
        # self.camera.start()

    def screenshot(self):
        self.frame = self.camera.grab()

    def get_pixel_from_screenshot(self, x, y):
        if self.frame is not None:
            return tuple(self.frame[y, x, :3])  # Zwraca kolor piksela jako (R, G, B)
        else:
            return (-1, -1, -1)

    def capture_screen(self):
        # frame = self.camera.get_latest_frame()  # Pobranie obrazu ekranu
        frame = self.camera.grab()

        timestamp = time.strftime("%Y%m%d_%H%M%S")

        x, y = 100, 200  # Przykładowe współrzędne

        if frame is not None:
            pixel_color = frame[y, x, :3]  # :3 ignoruje kanał alfa, jeśli istnieje
            cv2.imwrite(f"screenshots/screenshot_{timestamp}.png", frame)
            print("Screenshot zapisany!")
            r, g, b = pixel_color
            print(f"Kolor piksela (R, G, B): ", r, g ,b)
        else:
            print("BLAD ZAPISU SCREENSHOT")

    def stop(self):
        self.camera.stop()
# cap = CaptureTest()
# cv2.imwrite("screenshot.png", cap.capture_screen())
# print("Zapisano screenshot!")

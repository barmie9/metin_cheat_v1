
class DinputKeys:
    def __init__(self, dinput_address):
        self.dinput_address = dinput_address
        self.metin_keys = {
            "1": (0x312BA, 128),
            "2": (0x312BB, 128),
            "3": (0x312BC, 128),
            "4": (0x312BD, 128),
            "F1": (0x312F3, 128),
            "F2": (0x312F4, 128),
            "F3": (0x312F5, 128),
            "F4": (0x312F6, 128),
            "F5": (0x312F7, 128),
            "F6": (0x312F8, 128),
            "F7": (0x312F9, 128),
            "F8": (0x312F3, 128),
            "z": (0x312E4, 128),
            "w": (0x312C9, 128),
            "s": (0x312D7, 128),
            "a": (0x312D6, 128),
            "d": (0x312D8, 128),
            "g": (0x312D8, 8388608),
            "ctrl": (0x312D4, 32768),
            "space": (0x312F0, 32768)
        }


    def get_key_address(self, key): # Zwraca None jeśli nie istnieje
        buf = self.metin_keys.get(key)
        key_offset = (buf[0] + self.dinput_address, buf[1])  # Tworzymy nową krotkę z pełnym adressem
        print("key_offset", key_offset)
        if key_offset != None:
            # return self.dinput_address + key_offset
            return key_offset
        else:
            return None

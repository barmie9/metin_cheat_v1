
class DinputKeys:
    def __init__(self, dinput_address):
        self.dinput_address = dinput_address
        self.metin_keys = {
            "1": (0x312BA, 128),
            "2": (0x312BB, 128),
            "3": (0x312BC, 128),
            "4": (0x312BD, 128),
            "f1": (0x312F3, 128),
            "f2": (0x312F4, 128),
            "f3": (0x312F5, 128),
            "f4": (0x312F6, 128),
            "f5": (0x312F7, 128),
            "f6": (0x312F8, 128),
            "f7": (0x312F9, 128),
            "f8": (0x312F3, 128),
            "z": (0x312E4, 128),
            "w": (0x312C9, 128),
            "s": (0x312D7, 128),
            "a": (0x312D6, 128),
            "d": (0x312D8, 128),
            "g": (0x312D8, 8388608),
            "ctrl": (0x312D4, 32768),
            "space": (0x312F0, 32768)
        }
        # cheat engine 2 bytes (te, ktore sa 32768 mozna na 1 byte):
        # 1 byte powinien byc lepszy do szukania
        self.virtual_metin_keys = {
            "1": (0x3025A, 128),# OK
            "2": (0x3025A, 32768),# OK
            "3": (0x3025C, 128),# OK
            "4": (0x312BD, 128),# TODO
            "f1": (0x30292, 32768),# OK
            "f2": (0x30294, 128),# OK
            "f3": (0x312F5, 128),# TODO
            "f4": (0x312F6, 128),# TODO
            "f5": (0x312F7, 128),# TODO
            "f6": (0x312F8, 128),# TODO
            "f7": (0x312F9, 128),# TODO
            "f8": (0x312F3, 128),# TODO
            "z": (0x30284, 128),# OK
            "w": (0x30268, 32768),# OK
            "s": (0x30276, 32768),# OK
            "a": (0x30276, 128),# OK
            "d": (0x30278, 128),# OK
            "g": (0x3027A, 128),# OK
            "q": (0x30268, 128),# OK
            "e": (0x3026A, 128),# OK
            "r": (0x3026A, 32768),# OK
            "ctrl": (0x30275, 128),# OK
            "space": (0x30290, 32768)# OK
        }


    def get_key_address(self, key, is_virtual_machine): # Zwraca None jeśli nie istnieje
        if is_virtual_machine:
            buf = self.virtual_metin_keys.get(key.lower())
        else:
            buf = self.metin_keys.get(key.lower())
        key_offset = (buf[0] + self.dinput_address, buf[1])  # Tworzymy nową krotkę z pełnym adressem
        print("key_offset", key_offset)
        if key_offset != None:
            # return self.dinput_address + key_offset
            return key_offset
        else:
            return None

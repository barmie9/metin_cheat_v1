# import ctypes
import ctypes.wintypes
import psutil

class MODULEINFO(ctypes.Structure):
    _fields_ = [("lpBaseOfDll", ctypes.c_void_p),
                ("SizeOfImage", ctypes.c_ulong),
                ("EntryPoint", ctypes.c_void_p)]

class CtypeService:
    def __init__(self):
        self.process_name = "Mt2009.exe"
        self.user32 = ctypes.windll.user32

    def get_process_pid(self,process_name):
        # Pobieranie listy wszystkich procesów
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                pid = proc.info['pid']
                break
        else:
            raise Exception(f"Proces {self.process_name} nie został znaleziony.")
            return 0
        print("Process : ", process_name, " PID: ", pid)
        return pid
    def get_base_address(self, process_name):
        self.process_name = process_name

        pid = self.get_process_pid(process_name)

        # # Funkcja OpenProcess
        # OpenProcess = ctypes.windll.kernel32.OpenProcess
        # OpenProcess.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD]
        # OpenProcess.restype = ctypes.wintypes.HANDLE

        # Otwieranie procesu
        PROCESS_ALL_ACCESS = 0x1F0FFF
        process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

        if not process_handle:
            # error_code = ctypes.windll.kernel32.GetLastError()
            raise Exception("Nie można otworzyć procesu. ")

        # Pobieranie uchwytów do modułów procesu
        hModule = ctypes.c_void_p()
        cbNeeded = ctypes.c_ulong()
        ctypes.windll.psapi.EnumProcessModules(process_handle, ctypes.byref(hModule), ctypes.sizeof(hModule), ctypes.byref(cbNeeded))

        # Pobieranie informacji o module
        module_info = MODULEINFO()
        ctypes.windll.psapi.GetModuleInformation(process_handle, hModule, ctypes.byref(module_info), ctypes.sizeof(module_info))

        # Zamykanie uchwytu do procesu
        ctypes.windll.kernel32.CloseHandle(process_handle)

        return module_info.lpBaseOfDll

    def get_module_address(self, process_name, module_name):
        # Pobieranie pid procesu
        pid = self.get_process_pid(process_name)

        # Otwieranie procesu
        PROCESS_ALL_ACCESS = 0x1F0FFF
        process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        if not process_handle:
            raise Exception("Nie można otworzyć procesu.")

        # Pobieranie uchwytów do modułów procesu
        hModule = (ctypes.c_void_p * 1024)()
        cbNeeded = ctypes.c_ulong()
        ctypes.windll.psapi.EnumProcessModulesEx(process_handle, ctypes.byref(hModule), ctypes.sizeof(hModule),
                                                 ctypes.byref(cbNeeded), 0x03)

        # Szukanie modułu po nazwie
        module_base_address = None
        for i in range(int(cbNeeded.value / ctypes.sizeof(ctypes.c_void_p))):
            module_filename = ctypes.create_unicode_buffer(255)
            ctypes.windll.psapi.GetModuleFileNameExW(process_handle, hModule[i], ctypes.byref(module_filename), 255)
            if module_name in module_filename.value:
                module_info = MODULEINFO()
                ctypes.windll.psapi.GetModuleInformation(process_handle, hModule[i], ctypes.byref(module_info),
                                                         ctypes.sizeof(module_info))
                module_base_address = module_info.lpBaseOfDll
                break

        # Zamykanie uchwytu do procesu
        ctypes.windll.kernel32.CloseHandle(process_handle)

        if not module_base_address:
            raise Exception(f"Moduł {module_name} nie został znaleziony w procesie {process_name}.")

        return module_base_address
    def focus_window(self, window_title): # Do poprawy/ moze antywirus/ może uprawnienia
        # Znalezienie okna po tytule
        hwnd = self.user32.FindWindowW(None, window_title)

        # Ustawienie okna w trybie focus
        if hwnd:
            self.user32.SetForegroundWindow(hwnd)
            return True
        else:
            print("Nie znaleziono okna o podanym tytule")
            return False

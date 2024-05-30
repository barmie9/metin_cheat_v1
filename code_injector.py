import pymem
import pymem.pattern
from keystone import Ks, KS_ARCH_X86, KS_MODE_32  # Użyj KS_MODE_64 dla 64-bitowych programów
import struct
from ctype_service import CtypeService

class CodeInjector:
    def __init__(self, process_name, process_pid):
        self.process_name = process_name
        self.process_pid = process_pid
        self.aob_pattern = bytes.fromhex("80 7F 78 00 74 07")  # Wzorzec bajtów z kodu jako obiekt bajtowy

        self.pm = pymem.Pymem()
        self.pm.open_process_from_id(process_pid)

        self.module = pymem.process.module_from_name(self.pm.process_handle, process_name)


    def assemble_code(self, asm_code):
        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        encoding, count = ks.asm(asm_code)
        return bytes(encoding)

    def find_pattern(self, pattern):
        module_address = self.module.lpBaseOfDll
        module_size = self.module.SizeOfImage
        pattern_address = pymem.pattern.pattern_scan_module(self.pm.process_handle, self.module, pattern)
        return pattern_address

    def inject_code(self, asm_code):
        # Znalezienie adresu wzorca bajtów
        address = self.find_pattern(self.aob_pattern)

        if address:
            print(f"Pattern found at address: {hex(address)}")

            # Przygotowanie pamięci dla nowego kodu
            new_mem_address = self.pm.allocate(0x1000)

            # Kompilacja kodu assemblera do bajtów
            injected_code = self.assemble_code(asm_code)
            print(f"Injected code: {injected_code}")

            # Wstrzyknięcie skompilowanego kodu do nowej pamięci
            self.pm.write_bytes(new_mem_address, injected_code, len(injected_code))

            # Modyfikacja oryginalnego kodu, aby skakał do nowej pamięci
            jmp_offset = new_mem_address - address - 5
            jmp_code = b'\xE9' + struct.pack("<i", jmp_offset) + b'\x90'
            print("jmp_code:: ", jmp_code)
            self.pm.write_bytes(address, jmp_code, len(jmp_code))
            # jmp_code = b'\xE9' + (new_mem_address - address - 5).to_bytes(4, byteorder='little') + b'\x90'
            # self.pm.write_bytes(address, jmp_code, len(jmp_code))

            print(f"Code injected at address: {hex(address)}")
        else:
            print("Pattern not found")

# Przykład użycia
if __name__ == "__main__":
    process_name = "CarolineMT2.exe"
    ctype_service = CtypeService()
    process_pid = ctype_service.get_process_pid(process_name)
    asm_code = """
    nop
    """

    injector = CodeInjector(process_name, process_pid)
    injector.inject_code(asm_code)

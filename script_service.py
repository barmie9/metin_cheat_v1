from memory_service import MemoryService
from thread_executor import ThreadExecutor

class ScriptService:
    def __init__(self):
        self.config_file_name = "config.txt"
        self.scripts_file_name = "scripts.txt"
        self.memory_service = MemoryService()
        self.scripts_list = self.load_scripts()
        self.thread_executor = ThreadExecutor()

        # self.execute_script("script_test")

    def load_scripts(self):
        scripts = {}
        try:
            with open(self.scripts_file_name, 'r', encoding='utf-8') as file:
                name = ''
                method = ''
                method_with_par = []
                param = []
                for line in file:
                    print(line.strip())
                    if line[0] == ',':
                        # print(" IF -> 1")
                        param.append(line.strip()[1:])
                    elif line[0] == '.' and method != '':
                        # print(" IF -> 2")
                        method_with_par.append((method, param))
                        param = []
                        method = line.strip()[1:]
                    elif line[0] == ':':
                        # print(" IF -> 3")
                        name = line.strip()[1:]

                    elif line[0] == '.':
                        # print(" IF -> 4")
                        method = line.strip()[1:]
                    elif line[0] == ';':
                        # print(" IF -> 5")
                        method_with_par.append((method, param))
                        scripts[name] = method_with_par
                        name = ''
                        method = ''
                        method_with_par = []
                        param = []
                    # print(scripts)

        except FileNotFoundError:
            print(f"Plik {self.scripts_file_name} nie został znaleziony.")
        except IOError:
            print(f"Wystąpił błąd podczas odczytu pliku {self.scripts_file_name}.")

        print(scripts)

        return scripts

    def execute_script(self, name, on):
        script = self.scripts_list[name]

        if self.thread_executor.is_script_queue_empty() and on:
            # Iteracja po każdej krotce w liście wartości
            for item in script:
                # self.memory_service.execute_method(item[0], item[1])
                self.thread_executor.add_function_to_script_queue(self.memory_service.execute_method, item[0], item[1])
                # print("    Metoda:", item[0])  # Pierwszy element krotki
                # print("    Parametry:", item[1])  # Drugi element krotki


    # def script_loop(self,name):
    #     script = self.scripts_list[name]
    #
    #     # Iteracja po każdej krotce w liście wartości
    #     for item in script:
    #         self.memory_service.execute_method(item[0], item[1])
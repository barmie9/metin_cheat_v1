# my_class.py
from ReadWriteMemory import ReadWriteMemory

from color_service import ColorService
from ctype_service import CtypeService
from dinput_keys import DinputKeys
from thread_executor import ThreadExecutor
from code_injector import  CodeInjector

import time

class MemoryService:
    def __init__(self):
        # self.process_name = "Samia.exe"
        self.process_name = "Mt2009.exe"

        self.ctype_service = CtypeService()
        self.process_address = self.ctype_service.get_base_address(self.process_name)
        self.code_injector = CodeInjector("Mt2009.exe", self.ctype_service.get_process_pid("Mt2009.exe"))



        self.rwm = ReadWriteMemory()
        self.process = self.rwm.get_process_by_name(self.process_name)
        self.process.open()

        self.thread_executor = ThreadExecutor()

        self.dinput_address = self.ctype_service.get_module_address(self.process_name,"DINPUT8.dll")
        self.dinput_keys = DinputKeys(self.dinput_address)

        self.pWalk1 = self.get_pointer(0x009CFB6C, [0xa0])
        self.pWalk2 = self.get_pointer(0x009CFB6C, [0xa4])
        self.pPositionX = self.get_pointer(0x009DA230, [0x3A0, 0x10])
        self.pPositionY = self.get_pointer(0x009DA230, [0x3a0, 0x14])
        self.pHp = self.get_pointer(0x02C67A88, [0x10, 0x24, 0x74, 0x2c, 0x78, 0x40]) # Max 60 do 0 przy 20% hp, Przy poniżej 20% Hp pokazuje duża liczbe

        self.methods_list = self.generate_method_list()

        self.position = (-1, -1)

        self.direction_positive = True

        self.color_service = ColorService(0,0)

    def display_process(self):
        print("Process name: " + self.process_name + " , Process address: " + str(hex(self.process_address)))

    def get_pointer(self, first_address, offsets):
        return self.process.get_pointer(self.process_address + first_address, offsets=offsets)

    def get_coordinate(self):
        self.position = (self.process.read(self.pPositionX),
                self.process.read(self.pPositionY))
        # print(self.position)
        return self.position

    def attack(self, is_on):
        if is_on:
            self.process.write(self.pWalk2, 1)
        else:
            self.process.write(self.pWalk2, 0)

    def attack(self, is_on):

        # is_on2 =bool(is_on)
        if is_on == 'True':
            print("T AttackT: ", is_on)
            self.thread_executor.add_function_to_queue(self.process.write, self.pWalk2, 1)
        else:
            print("T AttackF: ", is_on)
            self.thread_executor.add_function_to_queue(self.process.write, self.pWalk2, 0)

    def press_key(self, key):
        print("key", key)
        address, value = self.dinput_keys.get_key_address(key)

        print("value", address, value)
        self.process.write(address, value)

    def release_key(self, key):
        address, value = self.dinput_keys.get_key_address(key)
        self.process.write(address, 0)

    # def click_key(self, key, time_sec=0.01):
    #     print("Press: " , key)
    #     self.thread_executor.add_function_to_queue(self.press_key,key)
    #     self.thread_executor.add_function_to_queue(self.sleep, time_sec)
    #     self.thread_executor.add_function_to_queue(self.release_key, key)

    def click_key(self, key, time_sec):
        print("T Press: " , key)
        time = float(time_sec)
        self.thread_executor.add_function_to_queue(self.press_key,key)
        self.thread_executor.add_function_to_queue(self.sleep2, time)
        self.thread_executor.add_function_to_queue(self.release_key, key)

    def click_key_thread2(self, key, time_sec):
        time = float(time_sec)
        self.thread_executor.add_function_to_long_queue(self.press_key,key)
        self.thread_executor.add_function_to_long_queue(self.sleep2, time)
        self.thread_executor.add_function_to_long_queue(self.release_key, key)

    def click_key_not_thread(self, key, time_sec):
        print('click_key_not_thread: ', key, ', ', time_sec)
        time_s = float(time_sec)
        self.press_key(key)
        # self.sleep2, time
        time.sleep(time_s)
        self.release_key(key)

    def shortcut_key(self, key_1, key_2):
        self.press_key(key_1)
        time.sleep(0.03)
        self.press_key(key_2)
        time.sleep(0.02)
        self.release_key(key_1)
        self.release_key(key_2)

    def horse_key_execute(self):
        self.thread_executor.add_function_to_queue(self.shortcut_key, 'ctrl','g')


    def sleep2(self, time_sec):
        time_s = float(time_sec)
        time.sleep(time_s)
    # def sleep(self, time_sec):
    #     print("T Sleep: ",  time_sec)
    #     self.thread_executor.add_function_to_queue(self.sleep2, float(time_sec))

    def walk (self, direction):
        if direction == 0:
            # self.process.write(self.pWalk2, 65536)
            self.process.write(self.pWalk1, 0)
            return True

        self.process.write(self.pWalk2, 256)
        if direction == 1:
            self.process.write(self.pWalk1, 1)
        elif direction == 2:
            self.process.write(self.pWalk1, 16777217)
        elif direction == 3:
            self.process.write(self.pWalk1, 16777216)
        elif direction == 4:
            self.process.write(self.pWalk1, 16777472)
        elif direction == 5:
            self.process.write(self.pWalk1, 256)
        elif direction == 6:
            self.process.write(self.pWalk1, 65792)
        elif direction == 7:
            self.process.write(self.pWalk1, 65536)
        elif direction == 8:
            self.process.write(self.pWalk1, 65537)
        else:
            return False
        return True

    def walk_to_point(self, point):

        self.position = (self.process.read(self.pPositionX),
                         self.process.read(self.pPositionY))

        xSub = point[0] - self.position[0]
        ySub = point[1] - self.position[1]

        ac = 100
        if xSub > ac and ySub > ac:
            self.walk(4)
        elif xSub < (-ac) and ySub < (-ac):
            self.walk(8)
        elif xSub > ac and ySub < (-ac):
            self.walk(2)
        elif xSub < (-ac) and ySub > ac:
            self.walk(6)
        elif xSub > ac:
            self.walk(3)
        elif xSub < (-ac):
            self.walk(7)
        elif ySub > ac:
            self.walk(5)
        elif ySub < (-ac):
            self.walk(1)
        else:
            self.walk(0)
            return True

        return False

    def generate_method_list(self):
        # Przykładowe wywołanie: self.methods_list['click_key']("2", 0.01)
        return {
            'attack': self.attack,
            'click_key': self.click_key,
            'sleep': self.sleep2,
            'walk_to_point': self.walk_to_point,
            'click_key_not_thread': self.click_key_not_thread,
            'horse_key_execute': self.horse_key_execute
        }

    def execute_method (self, name, parameters):
        # print(name)
        # print(parameters)
        if(len(parameters) == 0):
            self.methods_list[name]()
        else:
            self.methods_list[name](*parameters)


    def change_direction(self):

        if self.direction_positive:
            # address, value = self.dinput_keys.get_key_address('s')
            # self.process.write(address, value)
            self.direction_positive = False
            self.click_key_thread2('s',0.5)
        else:
            self.direction_positive = True
            self.click_key_thread2('w', 0.5)
            # address, value = self.dinput_keys.get_key_address('w')
            # self.process.write(address, value)


    def inject_test(self):
        self.code_injector.inject_code()

    def update_color(self):
        x, y = self.color_service.get_mouse_position()
        print("Color cord: ", x, y)
        self.color_service.set_point(x, y)
        return self.color_service.update_color()

    def press_key_if_color_equal(self, key, time_sec):
        current_color = self.color_service.get_pixel_color()
        if self.color_service.is_color_equal(current_color):
            self.click_key(key, time_sec)
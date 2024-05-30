import threading
import queue

#### MOZLIWE ZE BEDZIE TRZEBA ZMIENIC NA KLASE STATYCZNA ZEBY PRZY TWORZENIU KAZDEGO OBIEKTU NIE TWORZYLY SIE NOWE WATKI !!!!!!
class ThreadExecutor:
    def __init__(self):
        # Utwórz kolejk zadań
        self.task_queue = queue.Queue()
        self.long_task_queue = queue.Queue()
        self.script_task_queue = queue.Queue()

        # Utwórz wąteki
        self.thread = threading.Thread(target=self.worker, args=(self.task_queue,))
        self.thread.start()

        self.long_thread = threading.Thread(target=self.long_worker, args=(self.long_task_queue,))
        self.long_thread.start()

        self.script_thread = threading.Thread(target=self.script_worker, args=(self.script_task_queue,))
        self.script_thread.start()

    def worker(self, queue):
        while True:
            # Pobierz zadanie z kolejki
            task = queue.get()
            # print("task: ", task)
            if task is None:
                break  # Jeśli otrzymasz specjalne zadanie None, wątek się zakończy
            # Wykonaj zadanie
            task()
            # Oznacz zadanie jako wykonane
            queue.task_done()

    def long_worker(self, queue):
        while True:
            # Pobierz zadanie z kolejki
            task = queue.get()
            if task is None:
                break  # Jeśli otrzymasz specjalne zadanie None, wątek się zakończy
            # Wykonaj zadanie
            task()
            # Oznacz zadanie jako wykonane
            queue.task_done()

    def script_worker(self, queue):
        while True:
            # Pobierz zadanie z kolejki
            task = queue.get()
            if task is None:
                break  # Jeśli otrzymasz specjalne zadanie None, wątek się zakończy
            # Wykonaj zadanie
            task()
            # Oznacz zadanie jako wykonane
            queue.task_done()

    def add_function_to_queue(self, func, *args):
        self.task_queue.put(lambda: func(*args))

    def add_function_to_long_queue(self, func, *args):
        self.long_task_queue.put(lambda: func(*args))

    def add_function_to_script_queue(self, func, *args):
        self.script_task_queue.put(lambda: func(*args))

    def end_thread(self):
        # Dodaj specjalne zadanie None, aby zakończyć wątek
        self.task_queue.put(None)
        self.thread.join()

    def is_script_queue_empty(self):
        return self.script_task_queue.empty()

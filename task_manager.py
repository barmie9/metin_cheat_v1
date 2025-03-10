class TaskManager:
    def __init__(self, app):
        self.app = app
        self.after_ids = {}

    def toggle_task(self, task_name, interval, *args):
        """Włącza/wyłącza powtarzające się zadanie."""
        checkbox_var = getattr(self.app.gui_manager, f'checkbox_{task_name}_var', None)

        if checkbox_var and checkbox_var.get():
            self.after_ids[task_name] = self.method_repeater(task_name, interval, *args)
        elif task_name in self.after_ids:
            self.app.after_cancel(self.after_ids[task_name])
            del self.after_ids[task_name]

    def method_repeater(self, task_name, interval, *args):
        """Wykonuje metodę cyklicznie co zadany czas."""
        TASKS[task_name](self.app, *args)
        self.after_ids[task_name] = self.app.after(interval, self.method_repeater, task_name, interval, *args)
        return self.after_ids[task_name]


TASKS = {
    "pos": lambda app: app.memory_service.get_coordinate(),
    "walk": lambda app: app.memory_service.walk_to_point(57500, 64200),
    "key_z": lambda app: app.memory_service.click_key('z', 0.02),
    "key_f1": lambda app: app.memory_service.click_key('f1', 0.02),
    "key": lambda app: app.memory_service.click_key(app.gui_manager.entry_key.get(), 0.02),
    # "picup": lambda app: app.memory_service.click_key(app.gui_manager.entry.get(), 0.02),
}

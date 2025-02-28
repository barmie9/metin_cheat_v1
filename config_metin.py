import re
import ast


class MetinConfig:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = {}  # Przechowuje klucze i wartości
        self.lines = []  # Przechowuje wszystkie linie z pliku (w tym komentarze i puste linie)
        self.load_config()

    def load_config(self):
        """Wczytuje konfigurację z pliku, zachowując komentarze i puste linie."""
        with open(self.file_path, 'r') as file:
            for line in file:
                self.lines.append(line.strip())  # Dodajemy linię do listy lines
                line = line.strip()
                # Pomijanie pustych linii i komentarzy
                if not line or line.startswith('#'):
                    continue
                # Rozdzielanie klucza i wartości
                key_value = re.split(r'\s*=\s*', line, maxsplit=1)
                if len(key_value) == 2:
                    key, value = key_value
                    self.config[key.strip()] = self._parse_value(value.strip())

    def _parse_value(self, value):
        """Parsuje wartość do odpowiedniego typu (int, float, list, tuple, str)."""
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                try:
                    parsed_value = ast.literal_eval(value)
                    if isinstance(parsed_value, (list, tuple)):
                        return parsed_value
                except (ValueError, SyntaxError):
                    pass
        return value

    def get(self, key, default=None):
        """Pobiera wartość konfiguracji dla danego klucza."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Ustawia wartość konfiguracji dla danego klucza."""
        self.config[key] = value

    def save_config(self):
        """Zapisuje konfigurację do pliku, zachowując komentarze i puste linie."""
        with open(self.file_path, 'w') as file:
            for line in self.lines:
                # Jeśli linia zawiera klucz, który został zmodyfikowany, aktualizujemy ją
                if not line.startswith('#') and '=' in line:
                    key = line.split('=')[0].strip()
                    if key in self.config:
                        file.write(f"{key} = {self.config[key]}\n")
                        continue
                # W przeciwnym razie zapisujemy oryginalną linię (komentarz lub pustą linię)
                file.write(f"{line}\n")

    def print_config(self):
        """Wyświetla całą konfigurację w czytelny sposób."""
        print("Aktualna konfiguracja:")
        for key, value in self.config.items():
            print(f"{key} = {value}")

    def __str__(self):
        """Zwraca reprezentację konfiguracji jako string."""
        return "\n".join(f"{key} = {value}" for key, value in self.config.items())



# # Przykład użycia:
# if __name__ == "__main__":
#     config = MetinConfig('config.cfg')
#
#     # Wyświetlenie całej konfiguracji
#     config.print_config()
#
#     # Pobieranie wartości
#     print("\nPojedyncze wartości:")
#     print("Nazwa procesu:", config.get('PROCESS_NAME'))
#
#     # Edycja wartości
#     config.set('WAITING_TIME', 1.76)
#
#     # Zapisanie zmian
#     config.save_config()
#
#     # Wyświetlenie zaktualizowanej konfiguracji
#     print("\nZaktualizowana konfiguracja:")
#     config.print_config()
#     # print(config)
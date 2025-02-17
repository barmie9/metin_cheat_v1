import subprocess
import sys

# Lista bibliotek, które mogą wymagać instalacji
libraries = [
    "pymem",
    "keystone-engine",
    "mss",
    "psutil",
    "pygame",
    "pynput",
    "ReadWriteMemory",
    "dxcam" # pip install --upgrade dxcam comtypes
]

# Instalacja bibliotek za pomocą pip
for lib in libraries:
    subprocess.run([sys.executable, "-m", "pip", "install", lib], check=True)

print("Instalacja zakończona!")

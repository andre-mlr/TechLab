import signal
import sys
import os
from dotenv import load_dotenv
import tkinter as tk
from frontend import ChatApp

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função para lidar com sinal de interrupção (Ctrl+C)
def signal_handler(sig, frame):
    print('Você pressionou Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

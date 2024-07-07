import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from functools import partial
import os
import re
from dotenv import load_dotenv

# Importar funções do seu código existente
from info import register_user, login_user
from tutorials import get_tutorial
from reuniao import redirect_to_agenda_link
from rag import get_relevant_context_from_db, generate_rag_prompt, generate_answer

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Chave de API do YouTube (substitua pela sua chave)
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agente Conversacional")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        self.label_email = tk.Label(self.root, text="Email:")
        self.label_email.pack()
        self.entry_email = tk.Entry(self.root)
        self.entry_email.pack()

        self.label_password = tk.Label(self.root, text="Senha:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        self.btn_register = tk.Button(self.root, text="Registrar", command=self.register)
        self.btn_register.pack()

        self.btn_login = tk.Button(self.root, text="Login", command=self.login)
        self.btn_login.pack()

    def create_chat_screen(self, email):
        self.clear_screen()

        self.label_welcome = tk.Label(self.root, text=f"Bem-vindo, {email}!")
        self.label_welcome.pack()

        self.chat_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.chat_box.pack()

        self.entry_query = tk.Entry(self.root, width=50)
        self.entry_query.pack()

        self.btn_send = tk.Button(self.root, text="Enviar", command=partial(self.send_query, email))
        self.btn_send.pack()

        self.btn_logout = tk.Button(self.root, text="Logout", command=self.create_login_screen)
        self.btn_logout.pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def register(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        success, message = register_user(email, password)
        messagebox.showinfo("Registro", message)

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        success, message = login_user(email, password)
        if success:
            self.create_chat_screen(email)
        else:
            messagebox.showerror("Login", message)

    def send_query(self, email):
        query = self.entry_query.get()
        self.chat_box.config(state='normal')
        self.chat_box.insert(tk.END, f"Você: {query}\n")
        self.chat_box.config(state='disabled')
        self.entry_query.delete(0, tk.END)

        # Verificar se a query é uma solicitação de tutorial
        if "tutorial" in query.lower():
            tool_name = query.lower().replace("tutorial", "").strip()
            tutorials = get_tutorial(tool_name, YOUTUBE_API_KEY)
            self.display_response(tutorials)
        # Verificar se a query é uma solicitação de agendamento de reunião
        elif re.search(r"\bagendar reunião\b|\bmarcar reunião\b|\bagendar uma reunião\b|\bmarcar uma reunião\b", query, re.IGNORECASE):
            start_time_str = simpledialog.askstring("Input", "Informe a data e hora de início (formato YYYY-MM-DD HH:MM):")
            end_time_str = simpledialog.askstring("Input", "Informe a data e hora de término (formato YYYY-MM-DD HH:MM):")
            messages = redirect_to_agenda_link(email, start_time_str, end_time_str)
            for message in messages:
                self.display_response(message)
        else:
            context = get_relevant_context_from_db(query)
            prompt = generate_rag_prompt(query=query, context=context)
            answer = generate_answer(prompt=prompt)
            self.display_response(answer)

    def display_response(self, response):
        self.chat_box.config(state='normal')
        self.chat_box.insert(tk.END, f"Bot: {response}\n\n")
        self.chat_box.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

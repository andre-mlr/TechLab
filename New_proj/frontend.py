import tkinter as tk
from tkinter import messagebox
import webbrowser

class Frontend:
    def __init__(self, root, backend):
        self.root = root
        self.backend = backend
        self.user_id = None

        self.login_frame = tk.Frame(root)
        self.main_menu_frame = tk.Frame(root)

        self.create_login_frame()
        self.create_main_menu_frame()

    def create_login_frame(self):
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Email:").pack()
        self.entry_email = tk.Entry(self.login_frame)
        self.entry_email.pack()

        tk.Label(self.login_frame, text="Senha:").pack()
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.pack()

        tk.Button(self.login_frame, text="Registrar", command=self.register).pack()
        tk.Button(self.login_frame, text="Login", command=self.login).pack()

    def create_main_menu_frame(self):
        tk.Button(self.main_menu_frame, text="Agendar Reunião", command=self.schedule_meeting).pack()
        tk.Label(self.main_menu_frame, text="Pergunta ao Chat:").pack()
        self.entry_chat = tk.Entry(self.main_menu_frame)
        self.entry_chat.pack()
        tk.Button(self.main_menu_frame, text="Enviar", command=self.ask_chat).pack()

        tk.Label(self.main_menu_frame, text="Nome da Ferramenta para Tutorial:").pack()
        self.entry_tool = tk.Entry(self.main_menu_frame)
        self.entry_tool.pack()
        tk.Button(self.main_menu_frame, text="Obter Tutorial", command=self.get_tool_tutorial).pack()

        tk.Button(self.main_menu_frame, text="Sair", command=self.exit_program).pack()

    def register(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        if self.backend.register_user(email, password):
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Email já registrado. Por favor, faça login.")

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        if self.backend.login_user(email, password):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.user_id = self.backend.generate_user_id()
            self.show_main_menu()
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")

    def show_main_menu(self):
        self.login_frame.pack_forget()
        self.main_menu_frame.pack()

    def schedule_meeting(self):
        self.backend.redirect_to_agenda_link()
        messagebox.showinfo("Info", "Redirecionando para o link de agendamento...")

    def ask_chat(self):
        user_input = self.entry_chat.get()
        response = self.backend.handle_user_input(self.user_id, user_input)
        messagebox.showinfo("Resposta do Agente", response)

    def get_tool_tutorial(self):
        user_input = self.entry_tool.get()
        response = self.backend.get_tutorial(user_input)
        messagebox.showinfo("Tutorial", response)

    def exit_program(self):
        self.root.destroy()

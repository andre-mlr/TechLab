import tkinter as tk
from tkinter import messagebox
import webbrowser

class Frontend:
    def __init__(self, root, backend):
        self.root = root
        self.backend = backend
        self.user_id = None

        self.root.geometry("500x400")  # Definir o tamanho da janela

        self.login_frame = tk.Frame(root)
        self.main_menu_frame = tk.Frame(root)

        self.create_login_frame()
        self.create_main_menu_frame()

    def create_login_frame(self):
        self.login_frame.pack(pady=50)

        tk.Label(self.login_frame, text="Email:").pack(pady=5)
        self.entry_email = tk.Entry(self.login_frame)
        self.entry_email.pack()

        tk.Label(self.login_frame, text="Senha:").pack(pady=5)
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.pack()

        tk.Button(self.login_frame, text="Registrar", command=self.register).pack(pady=10)
        tk.Button(self.login_frame, text="Login", command=self.login).pack(pady=5)

    def create_main_menu_frame(self):
        self.main_menu_frame.pack(pady=60)

        tk.Button(self.main_menu_frame, text="Agendar Reunião", command=self.schedule_meeting).pack(pady=5)
        tk.Button(self.main_menu_frame, text="Conversar", command=self.ask_chat_menu).pack(pady=5)
        tk.Button(self.main_menu_frame, text="Obter Tutorial", command=self.get_tool_tutorial_menu).pack(pady=5)
        tk.Button(self.main_menu_frame, text="Sair", command=self.exit_program).pack(pady=5)

    def show_login_frame(self):
        self.main_menu_frame.pack_forget()
        self.login_frame.pack()

    def show_main_menu(self):
        self.login_frame.pack_forget()
        self.main_menu_frame.pack()

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

    def schedule_meeting(self):
        self.backend.redirect_to_agenda_link()
        messagebox.showinfo("Info", "Redirecionando para o link de agendamento...")

    def ask_chat_menu(self):
        self.main_menu_frame.pack_forget()
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(pady=50)

        tk.Label(chat_frame, text="Pergunta ao Chat:").pack(pady=5)
        entry_chat = tk.Entry(chat_frame)
        entry_chat.pack()

        def ask_chat():
            user_input = entry_chat.get()
            response = self.backend.handle_user_input(self.user_id, user_input)
            messagebox.showinfo("Resposta do Agente", response)
            chat_frame.pack_forget()
            self.main_menu_frame.pack()

        tk.Button(chat_frame, text="Enviar", command=ask_chat).pack(pady=10)

    def get_tool_tutorial_menu(self):
        self.main_menu_frame.pack_forget()
        tutorial_frame = tk.Frame(self.root)
        tutorial_frame.pack(pady=50)

        tk.Label(tutorial_frame, text="Escolha a Ferramenta para Tutorial:").pack(pady=5)

        tk.Button(tutorial_frame, text="Discord", command=lambda: self.get_specific_tutorial("Discord")).pack(pady=5)
        tk.Button(tutorial_frame, text="GitHub", command=lambda: self.get_specific_tutorial("GitHub")).pack(pady=5)
        tk.Button(tutorial_frame, text="Jira", command=lambda: self.get_specific_tutorial("Jira")).pack(pady=5)
        tk.Button(tutorial_frame, text="VSCode", command=lambda: self.get_specific_tutorial("VSCode")).pack(pady=5)

        tk.Button(tutorial_frame, text="Voltar ao Menu Principal", command=self.show_main_menu).pack(pady=10)

    def get_specific_tutorial(self, tool_name):
        api_key = "AIzaSyDT85Dr6Qh0qM4-orMhwIGqyJF04IQy4qE"
        response = self.backend.get_tutorial(tool_name, api_key)
        messagebox.showinfo(f"Tutorial de {tool_name}", response)

    def exit_program(self):
        self.root.destroy()

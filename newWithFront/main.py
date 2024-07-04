import json
import webbrowser
import tkinter as tk
from context_manager import context_manager
from knowledge_base import knowledge_base
from restrictions import restrictions
from llm_integration import llm_integration
from tutorials import get_tutorial as fetch_tutorial
from frontend import Frontend

USER_DATA_FILE = 'users.json'

def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def register_user(email, password):
    users = load_user_data()
    if email in users:
        return False
    users[email] = {'password': password}
    save_user_data(users)
    return True

def login_user(email, password):
    users = load_user_data()
    return email in users and users[email]['password'] == password

def handle_user_input(user_id, user_input):
    context_manager.add_message(user_id, user_input)
    if user_input.lower() == "agendar reunião":
        return redirect_to_agenda_link()
    knowledge_results = knowledge_base.search(user_input)
    if not knowledge_results:
        return "Desculpe, não consegui encontrar informações relevantes para sua pergunta."
    knowledge_context = "\n".join(knowledge_results)
    prompt = f"Contexto do usuário: {context_manager.get_user_context(user_id)}\nEntrada do usuário: {user_input}\nConhecimento relevante: {knowledge_context}\n"
    llm_response = llm_integration.query_model(prompt)
    response = restrictions.apply_restrictions(llm_response)
    context_manager.add_message(user_id, response)
    return response

def redirect_to_agenda_link():
    agenda_link = "https://calendar.app.google/JKixZym1Zm1L1GuNA"
    webbrowser.open_new_tab(agenda_link)

def generate_user_id():
    return context_manager.generate_user_id()

def get_tutorial(tool_name, api_key):
    return fetch_tutorial(tool_name, api_key)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Login e Registro")

    backend = type('Backend', (object,), {
        'register_user': register_user,
        'login_user': login_user,
        'handle_user_input': handle_user_input,
        'redirect_to_agenda_link': redirect_to_agenda_link,
        'generate_user_id': generate_user_id,
        'get_tutorial': get_tutorial
    })

    app = Frontend(root, backend)
    root.mainloop()

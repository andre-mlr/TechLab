import json
import os

# Nome do arquivo JSON para armazenar dados dos usuários
USER_DATA_FILE = 'user_data.json'

# Função para carregar os dados dos usuários
def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, 'r') as file:
        return json.load(file)

# Função para salvar os dados dos usuários
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file, indent=4)

# Função para registrar um novo usuário
def register_user(email, password):
    user_data = load_user_data()
    if email in user_data:
        return False, "Email já registrado."
    user_data[email] = {"password": password}
    save_user_data(user_data)
    return True, "Registro bem-sucedido."

# Função para fazer login
def login_user(email, password):
    user_data = load_user_data()
    if email not in user_data:
        return False, "Email não encontrado."
    if user_data[email]["password"] != password:
        return False, "Senha incorreta."
    return True, "Login bem-sucedido."

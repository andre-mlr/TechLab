import json
import getpass

# Nome do arquivo JSON onde os dados serão armazenados
USER_DATA_FILE = 'users.json'

# Função para carregar dados de usuários do arquivo JSON
def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Função para salvar dados de usuários no arquivo JSON
def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


# Função para registrar um novo usuário
def register_user():
    email = input("Digite seu email (será usado como nome de usuário): ")

    # Verificar se o email já existe
    users = load_user_data()
    if email in users:
        print("Email já registrado. Por favor, faça login.")
        return

    password = getpass.getpass("Digite sua senha: ")

    # Salvar os dados do novo usuário
    users[email] = {
        'password': password
    }

    save_user_data(users)
    print("Usuário registrado com sucesso!")

# Função para login de usuário
def login_user():
    email = input("Digite seu email: ")
    password = getpass.getpass("Digite sua senha: ")

    # Carregar os dados do usuário do arquivo JSON
    users = load_user_data()

    if email in users and users[email]['password'] == password:
        print("Login bem-sucedido!")
        return True
    else:
        print("Email ou senha incorretos.")
        return False

# Exemplo de uso na sua Main
if __name__ == "__main__":
    while True:
        escolha = input("1- Registrar\n2- Login\n3- Sair\n")
        
        if escolha == "1":
            register_user()
        elif escolha == "2":
            if login_user():
                # Login bem-sucedido, pode continuar com outras funcionalidades
                # Por exemplo, redirecionar para agendamento, perguntas, tutoriais, etc.
                continue
        elif escolha == "3":
            break

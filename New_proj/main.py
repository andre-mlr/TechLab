import json
import getpass
import webbrowser
from context_manager import context_manager
from knowledge_base import knowledge_base
from restrictions import restrictions
from llm_integration import llm_integration
from tutorials import get_tutorial

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
        return False

    password = getpass.getpass("Digite sua senha: ")

    # Salvar os dados do novo usuário
    users[email] = {
        'password': password
    }

    save_user_data(users)
    print("Usuário registrado com sucesso!")
    return True

# Função para login de usuário
def login_user():
    email = input("Digite seu email: ")
    password = getpass.getpass("Digite sua senha: ")

    # Carregar os dados do usuário do arquivo JSON
    users = load_user_data()

    if email in users and users[email]['password'] == password:
        print("Login bem-sucedido!")
        return email
    else:
        print("Email ou senha incorretos.")
        return None

def handle_user_input(user_id, user_input):
    context_manager.add_message(user_id, user_input)

    if user_input.lower() == "agendar reunião":
        return redirect_to_agenda_link()

    # Buscar contexto relevante na base de conhecimento
    knowledge_results = knowledge_base.search(user_input)
    if not knowledge_results:
        return "Desculpe, não consegui encontrar informações relevantes para sua pergunta."

    knowledge_context = "\n".join(knowledge_results)

    # Integrar com o modelo de linguagem
    prompt = f"Contexto do usuário: {context_manager.get_user_context(user_id)}\nEntrada do usuário: {user_input}\nConhecimento relevante: {knowledge_context}\n"
    llm_response = llm_integration.query_model(prompt)

    # Aplicar restrições
    response = restrictions.apply_restrictions(llm_response)
    context_manager.add_message(user_id, response)  # Adicionar resposta ao contexto
    return response

def redirect_to_agenda_link():
    # URL do link de agendamento
    agenda_link = "https://calendar.app.google/JKixZym1Zm1L1GuNA"

    # Abrir a URL no navegador padrão
    webbrowser.open_new_tab(agenda_link)

# Exemplo de uso
if __name__ == "__main__":
    while True:
        escolha = input("1- Registrar\n2- Login\n3- Sair\n")
        
        if escolha == "1":
            if register_user():
                print("Você pode fazer login agora.")
        elif escolha == "2":
            user_email = login_user()
            if user_email:
                user_id = context_manager.generate_user_id()
                test_prompt = "Hello, Groq!"
                test_response = handle_user_input(user_id, test_prompt)
                print(f"Teste de conexão: {test_response}")

                while True:
                    escolha = input("1- Agendar reunião\n2- Pergunta ao chat\n3- Tutoriais\n4- Sair\n")
                    if escolha == "1":
                        print("Redirecionando para o link de agendamento...")
                        redirect_to_agenda_link()
                        continue
                    elif escolha == '2':
                        user_input = input("Você: ")
                        response = handle_user_input(user_id, user_input)
                        print(f"Agente: {response}")
                    elif escolha == '3':
                        api_key = "AIzaSyDT85Dr6Qh0qM4-orMhwIGqyJF04IQy4qE"
                        user_input = input("Digite o nome da ferramenta (Github, Vscode, Jira, Discord): ")
                        response = get_tutorial(user_input, api_key)
                        print(f"Agente: {response}")
                    elif escolha == '4':
                        break
        elif escolha == "3":
            break

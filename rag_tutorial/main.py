import signal
import sys
import re
from dotenv import load_dotenv
import os



from rag import signal_handler, get_relevant_context_from_db, generate_rag_prompt, generate_answer
from info import register_user, login_user
from tutorials import get_tutorial
from reuniao import redirect_to_agenda_link

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Chave de API do YouTube (substitua pela sua chave)
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


# Função para lidar com sinal de interrupção (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

def main_menu():
    while True:
        print("\nSeja bem-vindo!!")
        print("1. Registrar")
        print("2. Login")
        print("3. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            email = input("Email: ")
            password = input("Senha: ")
            success, message = register_user(email, password)
            print(message)
        elif choice == '2':
            email = input("Email: ")
            password = input("Senha: ")
            success, message = login_user(email, password)
            if success:
                print(message)
                user_session(email)
            else:
                print(message)
        elif choice == '3':
            print("Até logo!")
            sys.exit(0)
        else:
            print("Opção inválida. Tente novamente.")

def user_session(email):
    while True:
        print(f"\nBem-vindo, {email}!")
        print("O que deseja perguntar?")
        query = input("Query: ")

        # Verificar se a query é uma solicitação de tutorial
        if "tutorial" in query.lower():
            tool_name = query.lower().replace("tutorial", "").strip()
            tutorials = get_tutorial(tool_name, YOUTUBE_API_KEY)
            print(tutorials)
        # Verificar se a query é uma solicitação de agendamento de reunião
        elif re.search(r"\bagendar reunião\b|\bmarcar reunião\b|\bagendar uma reunião\b|\bmarcar uma reunião\b", query, re.IGNORECASE):
            redirect_to_agenda_link(email)
        
        else:
            context = get_relevant_context_from_db(query)
            prompt = generate_rag_prompt(query=query, context=context)
            answer = generate_answer(prompt=prompt)
            print(answer)

if __name__ == "__main__":
    main_menu()

import openai

chave_api = "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"
openai.api_key = chave_api

def enviar_mensagem(mensagem, lista_mensagem=[]):
    lista_mensagem.append(
        {"role": "user", "content": mensagem}
    )

    resposta = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = lista_mensagem,
    )

    return resposta["choices"][0]["message"]

lista_mensagem = []

while True:
    texto = input("Escreva aqui sua mensagem:")

    if texto == "sair":
        break
    else:
        resposta = enviar_mensagem(texto, lista_mensagem)
        lista_mensagem.append(resposta)
        print("Chat:", resposta["content"])

# TechLab - Tutorial de funcionamento

1- Garantir que todas as bibliotecas utilizadas estejam instaladas na máquina, através do arquivo requirements.txt

2- na pasta onde os arquivos estão localizados, executar "python generate_embeddings.py" para que a pasta com os vetores de palavras seja criada(essa etapa deve demorar um pouco)

3- deve-se criar as chaves YOUTUBE_API_KEY e GROQ_API_KEY. Sobre a do Groq, deve-se utilizar do link disponibilizado no tutorial, e criar chave, e a do YouTube, deve-se criar um projeto no Google Cloud, ativar a YouTube Data API v3, e já aproveitar para ativar Google Calendar API. Então cria-se uma "CHAVE DE API".

4- para obter o arquivo credentials.json, deve-se criar uma chave no Google Cloud "IDs do cliente OAuth 2.0" e baixar o json gerado. Coloca-se ele na pasta com os arquivos e renomeia o arquivo para "credentials.json"

5- o arquivo token.pickle será gerado após a primeira execução do arquivo(da main.py), quando for solicitado um agendamento de reunião, um link aparecerá, onde a permissão será concedida e o arquivo gerado automaticamente. Após obtenção do arquivo, fecha-se o programa e roda-o novamente.

6- a respeito do agendamento, no arquivo "reuniao.py" o agendamento de reuniões é automaticamente direcionado ao meu email para facilitar a visualização de sucesso na solicitação, dessa forma, recomendo alterar o email para visualizar o resultado.

7- Após a configuração, executar "python main.py", e iniciar os testes de funcionamento(a primeira pergunta redirecionada aos embeddings é um pouco lenta, as demais são mais rápidas)

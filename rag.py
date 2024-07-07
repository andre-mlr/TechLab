import signal
import sys
from dotenv import load_dotenv
import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from groq import Groq

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
# Chave de API da Groq
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Função para lidar com sinal de interrupção (Ctrl+C)
def signal_handler(sig, frame):
    print('\nObrigado por usar Groq:')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Função para gerar o prompt para RAG
def generate_rag_prompt(query, context):
    escaped = context.replace("'","").replace('"',"").replace("\n"," ")
    prompt = ("""
    você é um chat informativo de questões usando texto. 
    Para responder a pergunta, use como referencia o contexto incluido
    aqui. Caso a pergunta seja desconexa com o contexto, apenas ignore
    a pergunta. Voce não está num chat técnico, use uma linguagem 
    amigável.
      QUESTION:'{query}'
      CONTEXT: '{context}'
      ANSWER:
                """).format(query=query, context=context)
    return prompt

# Função para buscar contexto relevante no banco de dados
def get_relevant_context_from_db(query):
    context = ""
    embedding_funcion = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device':'cpu'})
    vector_db = Chroma(persist_directory="chroma_db_nccn", embedding_function=embedding_funcion)
    search_results = vector_db.similarity_search(query, k=5)
    for result in search_results:
        context += result.page_content + "\n"
    return context

# Classe para integração com LLM da Groq
class LLMIntegration:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192"  

    def query_model(self, prompt):
        try:
            # Adicionando instrução para responder em português
            prompt_with_language = f"Por favor, responda em português.\n{prompt}"
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt_with_language,
                    }
                ],
                model=self.model,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Erro na requisição: {e}"

# Função para gerar resposta usando a classe LLMIntegration
def generate_answer(prompt):
    llm_integration = LLMIntegration(GROQ_API_KEY)
    return llm_integration.query_model(prompt)

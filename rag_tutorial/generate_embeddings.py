from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loaders = [PyPDFLoader('./base_v2.pdf')]

docs = []

for file in loaders:
    docs.extend(file.load())

text_splitter = RecursiveCharacterTextSplitter(chunk_size=600,chunk_overlap=60)
docs = text_splitter.split_documents(docs)
embedding_funcion = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device':'cpu'})

vectorstore = Chroma.from_documents(docs, embedding_funcion, persist_directory="./chroma_db_nccn")

#print(vectorstore._collection.count())
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.retrievers.multi_query import MultiQueryRetriever

if load_dotenv('.env'):
# for local development
    OPENAI_KEY=os.getenv('OPENAI_API_KEY')
else:
    OPENAI_KEY=st.secrets['OPENAI_API_KEY']

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=OPENAI_KEY)

### Provide the Bot with  CPF news from Oct 23 since GPT-4o mini has knowledge cutoff of October 2023
# Get the name of the files in the folder
dir_path = r'./News Releases'
filename_list = []

# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        filename_list.append(path)

# Load PDF documents
list_of_documents_loaded = []

for filename in filename_list:
    if filename.endswith('.pdf'): 
        try:
            # Load the document
            pdf_path = os.path.join(dir_path, filename)
            loader = PyPDFLoader(pdf_path)
            data = loader.load()
            list_of_documents_loaded.extend(data)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue

#Split the documents into smaller chunks (current doc no need splitting, provsion for new documents)
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents_chunked = splitter.split_documents(list_of_documents_loaded)

# Create embeddings and vector database
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
vectordb = Chroma.from_documents(
    documents=list_of_documents_loaded,
    embedding=embeddings_model,
    collection_name="naive_splitter", 
    persist_directory="./vector_db"
)


# Create the RAG chain
llm_model = ChatOpenAI(model='gpt-4o-mini', temperature=0, seed=42)
rag_chain = RetrievalQA.from_llm(
    retriever=vectordb.as_retriever(), llm=llm_model
)

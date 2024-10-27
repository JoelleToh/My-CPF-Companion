import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from functions.Vectordb import rag_chain
from functions.utility import check_password
from functions.llm import get_completion
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="CPF Policy Assistant"
)
# Check if the password is correct.  
if not check_password():
    st.stop()

# endregion <--------- Streamlit App Configuration --------->

st.title("📚 My CPF Policy Assistant")

# Input form for user query
form = st.form(key="form")
form.subheader("CPF Policy Explainer")
user_prompt2 = form.text_area("Enter your query regarding CPF Policy here", height=200)
# Initialize session state if not already done
if 'LLM_reply' not in st.session_state:
    st.session_state['LLM_reply'] = ''  # Previous LLM reply

if 'user_prompt1' not in st.session_state:
    st.session_state['user_prompt1'] = ''  # Previous user input

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = ''  # Complete conversation history


if form.form_submit_button("Submit"):
    # System message guiding the chatbot's behavior
    system_message = """You are a helpful assistant from the Central Provident Fund (CPF) of Singapore,\
    you are well versed in CPF Policy. 

    Understand the customer service query and decide if the query is related to CPF policy.
    If it is, proceed to reply using information from https://www.cpf.gov.sg/ and ensure it's based on Singapore context.
    If it's not related to CPF policy, reply: 'I'm unable to assist as the enquiry is not related to CPF policy.'
    """
    
    # Use RAG to process only the latest user query (user_prompt2)
    retrieved_docs = rag_chain.invoke(user_prompt2)  # RAG retrieves relevant info based on the latest query

    # Combine the conversation history with the retrieved information
    conversation_history_with_retrieval = (
        f"{system_message}\n"
        f"{st.session_state['conversation_history']}\n"
        f"User: {user_prompt2}\n"
        f"Retrieved Info: {retrieved_docs}"
    )

    # Feed the conversation history and retrieved docs into the LLM
    response = get_completion(conversation_history_with_retrieval)  # Use the LLM to generate a response

    # Update session state with the new user input and LLM response
    st.session_state['user_prompt1'] = user_prompt2  # Store current user input
    st.session_state['LLM_reply'] = response  # Store LLM's current response

    # Update the conversation history to include the new exchanges
    st.session_state['conversation_history'] += f"\nUser: {user_prompt2}\nAssistant: {response}"

    # Display the response generated by the RAG-enhanced LLM onto the frontend
    st.write(response)
    
    print(f"User Input is {user_prompt2}")
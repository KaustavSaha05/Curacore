# chatbot.py

import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_FAISS_PATH = "vectorstore/db_faiss"
MODEL_NAME = "llama3-8b-8192"

CUSTOM_PROMPT_TEMPLATE = """
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer.
Dont provide anything out of the given context.

Context: {context}
Question: {question}

Start the answer directly. No small talk please.
"""

# 1. Load the QA Chain (only once when the server starts) 
# Load the vector store
embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

# Load model
llm = ChatGroq(
    model_name=MODEL_NAME,
    temperature=0.5,
)

# prompt
prompt = PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "question"])

# final QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={'k': 3}),
    return_source_documents=False, 
    chain_type_kwargs={'prompt': prompt}
)

# 2.Reusable Function ---
def get_chatbot_response(input_text: str) -> str:
    """
    This function takes a user's question, sends it to the QA chain,
    and returns the final answer.
    """
    try:
        response = qa_chain.invoke({'query': input_text})
        return response.get("result", "Sorry, I couldn't process the answer.")
    except Exception as e:
        print(f"Error during QA chain invocation: {e}")
        return "An error occurred while trying to find an answer."

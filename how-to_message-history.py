# Baseado em https://python.langchain.com/v0.2/docs/how_to/message_history/

# Pegando chaves
from dotenv import load_dotenv
load_dotenv()
import os

# Tentarei já conectar com Supabase - Postgres
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

#Importando bibliotecas
import uuid
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

#Importando e definindo modelo
from langchain_openai import ChatOpenAI #OpenAI chat model integration.
model = ChatOpenAI(
    model="gpt-3.5-turbo", #Name of OpenAI model to use.
    temperature=0.7 #Sampling temperature
)

user_id = os.environ.get("user_id")

#Pegando todas as sessões do usuário
sessions_data = (
    supabase.table("chatbot_sessions")
    .select("id")
    .eq("user_id", user_id)
    .execute()
)
#print(sessions_data.data)


session_id = sessions_data.data[0]["id"]

#Pegando todas as mensagens de uma sessão de um usuário
messages_data = (
    supabase.table("chatbot_messages")
    .select("*")
    .eq("session_id", session_id)
    .order("created_at")
    .execute()
)

messages_list = messages_data.data

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


from utils import format_messages_history

print(format_messages_history(messages_list))
import uuid
from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client

user_id = os.environ.get("user_id")
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

#Função para criar novas sessões no Supabase
def create_session(user_id, name="Nova sessão", is_anonymous=False):
    myuuid = str(uuid.uuid4())
    session_creation = (
        supabase.table("chatbot_sessions")
        .insert({"id": myuuid, "user_id": user_id, "session_name": name,"is_anonymous": is_anonymous})
        .execute()
    )
    return myuuid

#Função para pegar as sessões de um usuário específico no Supabase
def get_sessions(user_id):
    sessions_list = (
        supabase.table("chatbot_sessions")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    return sessions_list

# Função para pegar as mensagens de uma sessão específica no Supabase. 
# Situação em que o usuário quer abrir uma sessão antiga
def get_session_messages(session_id):
    messages_data = (
        supabase.table("chatbot_messages")
        .select("*")
        .eq("session_id", session_id)
        .execute()
    )
    return messages_data.data

# Função para formatar as mensagens de uma sessão anterior no formato de messages_history
def format_messages_history(messages_list):
    messages_history = ""
    for i in messages_list:
        sender = i["message_sender"]
        content = i["content"]
        messages_history += f"{sender}: {content}\n"
    return messages_history

#USAR GPT PARA GERAR TÍTULO (NOME) PARA SESSÕES COM BASE NAS MENSAGENS
# def create_session_name():
#     session_name = gerar título usando gpt com base nas mensagens
#     return session_name

#Função para atualizar o nome de uma sessão no Supabase
def update_session(session_id, new_name):
    session_update = (
        supabase.table("chatbot_sessions")
        .update({"session_name": new_name})
        .eq("id", session_id)
         .execute()
    )
    return session_update

#Função para salvar as memórias sobre um usuário específico no Supabase. Serve para as memórias inicias ou novas
def save_memory(user_id, memories, session_id, origin):
    memory_saving = (
        supabase.table("user_memories")
        .insert({"user_id": user_id, "memories": memories,"session_id": session_id,"origin": origin})
        .execute()
    )
    return memory_saving

#Função para pegar as memórias sobre um usuário específico no Supabase
def get_memories(user_id):
    memories = (
        supabase.table("user_memories")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    return memories

#Função para salvar as mensagens de uma sessão no Supabase, tanto do Human quanto do Assistant
def save_message(user_id, session_id, message_sender, content, prompt_id):
    message_saving = (
        supabase.table("chatbot_messages")
        .insert({"user_id": user_id, "session_id": session_id, 
                 "message_sender": message_sender,"content": content, "prompt_id": prompt_id})
        .execute()
    )
    return message_saving

#Função para pegar o main prompt mais recente
def retrieve_prompt_main():
    prompt_data = (
        supabase.table("prompt_templates")
        .select("id, content")
        .eq("name", "main")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return prompt_data.data[0]

#Função para pegar o prompt que gera first_memories mais recente
def retrieve_prompt_first_memories():
    prompt_data = (
        supabase.table("prompt_templates")
        .select("id, content")
        .eq("name", "first_memories")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return prompt_data.data[0]
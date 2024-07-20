from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client
from utils import get_session_messages, format_messages_history, retrieve_prompt_main, get_memories, save_message
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", temperature=0.7)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

user_id = os.environ.get("user_id")
session_id = "xxx" #transformar numa variável do webapp com base em qual chat o usuário clicar na lista do histórico
current_session_id = session_id  #transformar numa variável do webapp com base em qual chat o usuário clicar na lista do histórico
chat_messages_list = get_session_messages(current_session_id) #usar esse dado para mostrar o chat na UI
formatado = format_messages_history(chat_messages_list)

#chain com prompt principal, para conversa entre humano e IA
prompt_main = retrieve_prompt_main()
prompt_main_id = prompt_main["id"]
prompt_main_content = prompt_main["content"]
main_prompt = ChatPromptTemplate.from_template(prompt_main_content)
main_chain = main_prompt | model

response_get_memories = get_memories(user_id)
string_memories = str(response_get_memories.data[0]["memories"])  #e quando tiver mais de uma linha de memórias??????????
memories = ""
memories += f"{string_memories}\n"

messages_history = formatado
while True:
    user_input = input("Para sair digite exit. Digite aqui: ")
    if user_input.lower() == 'exit':
        #chamar prompt que gera memória com base nas mensagens da sessão (ainda preciso fazer) e salvar no Supabase user_memories
        #chamar prompt que cria título da sessão (ainda preciso fazer) e salvar no Supabase user_memories
        break
    main_chain_response = main_chain.invoke({"memories":memories,"messages_history":messages_history,"input":user_input})
    messages_history += f"Human: {user_input}\n"
    messages_history += f"Assistant: {main_chain_response.content}\n"
    save_message(user_id, current_session_id, "Human", user_input, prompt_id=None)
    save_message(user_id, current_session_id, "Assistant", main_chain_response.content, prompt_main_id)
    print("Assistant: " + main_chain_response.content)
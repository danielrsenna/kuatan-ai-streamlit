from dotenv import load_dotenv
load_dotenv()
import os
from utils import save_memory, retrieve_prompt_first_memories

from supabase import create_client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o",temperature=0.7)
parser = JsonOutputParser()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


user_id = os.environ.get("user_id") #transformar isso numa variável do webapp

#chain com prompt para extrair memórias de primeiro contato com usuário
prompt_memories = retrieve_prompt_first_memories()
memories_langchain = ChatPromptTemplate.from_template(prompt_memories, partial_variables={"format_instructions": parser.get_format_instructions()})
memories_chain = memories_langchain | model | parser

user_input = input("Conte um pouco sobre você: ") #transformar numa variável do webapp
memories_chain_response = memories_chain.invoke({"input":user_input})
save_memory(
    user_id=user_id, 
    memories=memories_chain_response,
    session_id=None,
    origin=user_input
    )
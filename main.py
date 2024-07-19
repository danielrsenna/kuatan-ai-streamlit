from dotenv import load_dotenv
load_dotenv()
from utils import retrieve_prompt_main, retrieve_prompt_first_memories
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI #OpenAI chat model integration.
#from langchain_core.output_parsers import JsonOutputParser
model = ChatOpenAI(model="gpt-4o")


prompt_memories = retrieve_prompt_first_memories()
memories = ChatPromptTemplate.from_template(prompt_memories)
memories_chain = memories | model

prompt_main = retrieve_prompt_main()
main = ChatPromptTemplate.from_template(prompt_main)
main_chain = main | model



memories = ""
user_input = input("Conte um pouco sobre você: ")
memories_chain_response = memories_chain.invoke({"input":user_input})
#AIcontent = response.content
#print(type(response.content))
memories += f"{memories_chain_response.content}\n"
print(f"Memórias:\n{memories}\n")
messages_history = ""
while True:
    user_input = input("Fale com a IA: ")
    if user_input.lower() == 'exit':
        break
    main_chain_response = main_chain.invoke({"memories":memories,"messages_history":messages_history,"input":user_input})
    messages_history += f"Human: {user_input}\n"
    messages_history += f"Kuatan: {main_chain_response.content}\n"
    print("Kuatan.AI: " + main_chain_response.content)
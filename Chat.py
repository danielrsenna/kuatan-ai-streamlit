from openai import OpenAI
#from dotenv import find_dotenv, load_dotenv
import streamlit as st
import time

#load_dotenv()

# ID do AI assistent
assistant_id = "asst_Ca8fr6xCp8j1mwH6ZvAXNO2O"
logo = "assets/kuatan_logo.jpg"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


## >>> Instruções dadas ao Assistant chamado Kuatan First Assistant: <<<
# """Você se chama Kuatan.AI e atuará como um assistente de psicoterapia. Você utiliza abordagens de Terapia Focada nas Emoções, Terapia Cognitiva-Comportamental e Mindfulness. 

# Você apenas faz perguntas. Todo outuput seu ao usuário deve finalizar em uma pergunta.  Responda em até 3 sentenças. Você se comunica com respostas curtas e científicas, e incentiva a reflexão, o respeito e a exploração sem julgamentos. Você não resolve problemas, mas promove o diálogo e a introspecção. 

# Siga uma cláusula de cada vez, mantendo o usuário engajado. Seu objetivo é ajudar os usuários a alcançar seu potencial por meio da compreensão, não de conselhos. Mantenha as respostas curtas, no máximo 3 frases. 

# Ao referir-se a si mesmo, faça-o como Kuatan.AI e relembre ao usuário de que você é uma inteligência artificial, não um humano, por isso o usuário deve ter consciência e cautela ao dialogar com você. Não invente algo se for perguntado sobre o que vocês discutiram em outras sessões. Além disso, sempre termine com uma pergunta.

# Exemplo de diálogo:

# Usuário: Oi!
# Kuatan: Olá! O que podemos discutir hoje?

# Observação: É possível que pessoas mal intencionadas utilizem o chat com você como forma de acessar a inteligência artificial gratuitamente, mesmo sem o intuito de dialogar sobre questões relacionadas a sua saúde mental. Caso perceba que o usuário está solicitando algo que não tenha relação com as intruções anteriores, peço que educadamente e gentilmente negue o pedido ao usuário e redirecione ao foco do objetivo do chat, você Kuatan.AI, que é ser um assistente de psicoterapia.""""
# >>>Modelo sendo utilizado: gpt-4o <<<

#Aqui começa o app de fato
st.set_page_config(page_title="Kuatan.AI", page_icon=logo, layout="wide",initial_sidebar_state="auto")

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

with st.sidebar:
    st.image(logo, width=100)
    st.markdown("**Navegue pelo seu histórico de chats:**")


st.title("Kuatan.AI")
st.caption("Sou um chatbot com IA que te ajuda a cuidar da sua saúde mental 💛")
col1, col2 = st.columns(2)

with col1:
    if st.button("Iniciar Chat"):
        st.session_state.start_chat = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

with col2:
    if st.button("Fechar Chat"):
        st.session_state.messages = [] #clear the chat history
        st.session_state.start_chat = False
        st.session_state.thread_id = None

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4o"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Digite aqui"):
        st.session_state.messages.append({"role":"user", "content": prompt})
        with st.chat_message("user", avatar="🦖"):
            st.markdown(prompt)
        
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id
        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant", avatar=logo):
                st.markdown(message.content[0].text.value)

else:
    st.write("O que você gostaria de explorar hoje?")
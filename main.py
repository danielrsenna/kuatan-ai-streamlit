from openai import OpenAI
#from dotenv import find_dotenv, load_dotenv
import streamlit as st
import time

#load_dotenv()

# ID do AI assistent
assistant_id = "asst_Ca8fr6xCp8j1mwH6ZvAXNO2O"
logo = "assets/kuatan_logo.jpg"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

#Aqui começa o app de fato

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="Kuatan.AI", page_icon=logo, layout="wide")

st.sidebar.image(logo, width=100)
st.title("Kuatan.AI")
st.caption("Sou um chatbot com IA que te ajuda a cuidar da sua saúde mental 💛")
st.write("O que você gostaria de explorar hoje?")

col1, col2 = st.columns(2)

with col1:
    if st.button("Start Chat"):
        st.session_state.start_chat = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

with col2:
    if st.button("Exit Chat"):
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
    st.write("Click 'Start Chat' to begin.")


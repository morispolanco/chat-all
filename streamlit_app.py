import openai 
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 Chatbot") 

# Define the prompt here
prompt = "Diseña mensajes promocionales para un nuevo producto, adaptándolos a las características y audiencia de cada red social. \
Destaca sus propiedades únicas y ventajas para capturar la atención y generar el interés del consumidor. Usa técnicas de persuasión y \
creatividad para impactar eficazmente en cada plataforma."

if "messages" not in st.session_state:
    # The assistant begins the conversation with the prompt.
    st.session_state["messages"] = [{"role": "assistant", "content": prompt}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)

import openai 
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 Chatbot") 

# Define the prompts here
primer_prompt = "Hola, estoy aquí para ayudarte a diseñar mensajes promocionales para tu nuevo producto. Primero, \
necesito algunas informaciones. ¿Podrías decirme el nombre y las características principales de tu producto?"

segundo_prompt = "¡Genial! Ahora, dime quienes son la audiencia objetivo para este producto y qué plataformas de \
redes sociales planeas usar para la promoción."

if "messages" not in st.session_state:
    # The assistant begins the conversation with the first prompt.
    st.session_state["messages"] = [{"role": "assistant", "content": primer_prompt}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    if len(st.session_state.messages) == 2:  # If assistant has asked first question
        st.session_state.messages.append({"role": "assistant", "content": segundo_prompt})
        st.chat_message("assistant").write(segundo_prompt)
    else:
        # Get responses from chat model
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg.content)

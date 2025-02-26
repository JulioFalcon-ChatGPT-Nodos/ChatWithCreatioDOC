import os

import streamlit as st

from chatbot import Chatbot
from embedding import Embedder


class Sidebar:
    MODEL_OPTIONS = ["gpt-3.5-turbo", "gpt-4"]
    TEMPERATURE_MIN_VALUE = 0.0
    TEMPERATURE_MAX_VALUE = 1.0
    TEMPERATURE_DEFAULT_VALUE = 0.0
    TEMPERATURE_STEP = 0.01

    @staticmethod
    def about():
        about = st.sidebar.expander("Acerca de 🤖")
        sections = [
            "#### Chatea con Creatio DOCS es un chatbot de IA con memoria conversacional, diseñado para permitir a las personas que necesitan información " 
            "de primera mano relacionada con Creatio, puedan usarlo para en su dia a dia o en su entrenamiento para certificarse.📄",
            "#### Desarrollo efectuado por No Code-Services para sus clientes, usando Langchain, OpenAI y Streamlit."
            ,
        ]
        for section in sections:
            about.write(section)

    def model_selector(self):
        model = st.selectbox(label="Modelo", options=self.MODEL_OPTIONS)
        st.session_state["model"] = model

    @staticmethod
    def reset_chat_button():
        if st.button("Reset chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)

    def temperature_slider(self):
        temperature = st.slider(
            label="Temperatura, te recomendo usar 0",
            min_value=self.TEMPERATURE_MIN_VALUE,
            max_value=self.TEMPERATURE_MAX_VALUE,
            value=self.TEMPERATURE_DEFAULT_VALUE,
            step=self.TEMPERATURE_STEP,
        )
        st.session_state["temperature"] = temperature

    def show_options(self):
        with st.sidebar.expander("🛠️ OpenAI Config", expanded=True):
            self.reset_chat_button()
            self.model_selector()
            self.temperature_slider()
            st.session_state.setdefault("Model", self.MODEL_OPTIONS[0])
            st.session_state.setdefault("Temperature", self.TEMPERATURE_DEFAULT_VALUE)


class Utilities:
    @staticmethod
    def load_api_key():
        """
        Loads the OpenAI API key from the .env file or from the user's input
        and returns it
        """
        if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
            user_api_key = os.environ["OPENAI_API_KEY"]
            st.sidebar.success("API key cargada en forma local, desde .env", icon="🚀")
        else:
            user_api_key = st.sidebar.text_input(
                label="#### OpenAI API KEY 👇", placeholder="Introduce tu API key de openAI, empieza por sk-", type="password"
            )
            if user_api_key:
                st.sidebar.success("API key cargada", icon="🚀")
        return user_api_key

    @staticmethod
    def handle_upload():
        """
        Handles the file upload and displays the uploaded file
        """
        uploaded_file = st.sidebar.file_uploader("upload", type="pdf", label_visibility="collapsed")
        if uploaded_file is not None:
            pass
        else:
            st.sidebar.info(
                "Sube tus manuales de Creatio, en formato PDF, para empezar", icon="👆"
            )
            st.session_state["reset_chat"] = True
        return uploaded_file

    @staticmethod
    def setup_chatbot(uploaded_file, model, temperature):
        """
        Sets up the chatbot with the uploaded file, model, and temperature
        """
        embeds = Embedder()
        with st.spinner("Procesando..."):
            uploaded_file.seek(0)
            file = uploaded_file.read()
            vectors = embeds.getDocEmbeds(file, uploaded_file.name)
            chatbot = Chatbot(model, temperature, vectors)
        st.session_state["ready"] = True
        return chatbot

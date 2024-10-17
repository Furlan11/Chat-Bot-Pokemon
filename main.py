import streamlit as st
from streamlit_chat import message
from core import run_llm

# Personalización del fondo con una URL de imagen directa
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://www.google.com/imgres?q=pokedex%20fondo%20de%20pantalla&imgurl=https%3A%2F%2Fi.pinimg.com%2F736x%2Fa1%2F46%2Fe2%2Fa146e24a7dd962e772a5545256915fd1.jpg&imgrefurl=https%3A%2F%2Fmx.pinterest.com%2Fpin%2F986218018372984714%2F&docid=BF5E7wbvTNYLiM&tbnid=XNYx0EecQ3to4M&vet=12ahUKEwioq76ZlpaJAxVRgoQIHT85Cb4QM3oECGUQAA..i&w=636&h=1255&hcb=2&ved=2ahUKEwioq76ZlpaJAxVRgoQIHT85Cb4QM3oECGUQAA'); /* Reemplaza con tu URL de imagen directa */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    /* Personalización de los mensajes del usuario */
    .message__user {
        background-color: #ADD8E6 !important; /* Light blue */
        color: black !important;
    }
    /* Personalización de los mensajes del bot */
    .message__bot {
        background-color: #F0E68C !important; /* Khaki */
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Pokemon - Documentation Helper Bot")

# Personalizar el cuadro de entrada de texto
prompt = st.text_input(
    "Prompt",
    placeholder="Enter your prompt here",
    help="Ask me anything related to Pokemon!"
)

# Inicializar estados de sesión
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Función para crear una cadena con las fuentes
def create_sources_string(source_urls: set[str]) -> str:
    if not source_urls:
        return ""
    return "Sources:\n" + "\n".join(f"{i + 1}. {src}" for i, src in enumerate(sorted(source_urls)))

# Procesar el prompt y generar la respuesta del bot
if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(query=prompt, chat_history=st.session_state["chat_history"])

    # Extraer fuentes de los documentos
    sources = {doc.metadata["source"] for doc in generated_response["source"]}
    formatted_response = (
        f"{generated_response['result']}\n\n{create_sources_string(sources)}"
    )

    # Guardar el historial de prompts y respuestas
    st.session_state["user_prompt_history"].append(prompt)
    st.session_state["chat_answers_history"].append(formatted_response)
    st.session_state["chat_history"].append(("human", prompt))
    st.session_state["chat_history"].append(("ai", generated_response["result"]))

# Mostrar mensajes previos y personalizar los colores mediante CSS
if st.session_state["chat_answers_history"]:
    for user_query, response in zip(
        st.session_state["user_prompt_history"], st.session_state["chat_answers_history"]
    ):
        # Mensaje del usuario con avatar personalizado
        message(
            user_query,
            is_user=True,
            avatar_style="adventurer-neutral",  # Estilo del avatar del usuario
            key=f"user_{user_query}"
        )
        # Mensaje del bot con avatar personalizado
        message(
            response,
            is_user=False,
            avatar_style="bottts",  # Estilo del avatar del bot
            key=f"bot_{response}"
        )

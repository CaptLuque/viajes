import streamlit as st
import requests
import uuid
from PIL import Image
import os
import base64
from io import BytesIO

# Constants
WEBHOOK_URL = "HTTPS://cs-n8n-pro.onrender.com:443/webhook/0a16fb34-dbe4-47b3-aa75-448c2bf1b505"
BEARER_TOKEN = "viajesCamino1"

def generate_session_id():
    return str(uuid.uuid4())

def send_message_to_llm(session_id, message):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "sessionId": session_id,
        "chatInput": message
    }
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["output"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def get_image_as_base64(img, width=70):
    """Convierte una imagen PIL a base64 para mostrarla en HTML"""
    buffered = BytesIO()
    # Redimensionar la imagen manteniendo la proporción
    img_ratio = img.width / img.height
    new_width = width
    new_height = int(new_width / img_ratio)
    img_resized = img.resize((new_width, new_height))
    img_resized.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def main():
    # Cargar imágenes
    try:
        # Verificar si los archivos existen
        if not os.path.exists("Principal Turquesa_1.png"):
            st.warning("No se encuentra el archivo 'Imago Borde Blanco.png'")
        if not os.path.exists("logo.webp"):
            st.warning("No se encuentra el archivo 'logo.webp'")
        
        # Intentar cargar las imágenes
        img1 = Image.open("Principal Turquesa_1.png")
        img2 = Image.open("logo.webp")
        
        # Mostrar la primera imagen centrada en la barra lateral con texto debajo
        img1_base64 = get_image_as_base64(img1, width=90)
        st.sidebar.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                <img src="data:image/png;base64,{img1_base64}" width="300">
                <p style="margin-top: 5px; font-weight: bold; font-size: 1.4rem;">Viajes Camino de Santiago</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Mostrar la segunda imagen en la parte superior derecha
        _, _, _, _, col5 = st.columns(5)
        with col5:
            st.image(img2, width=390)
    except FileNotFoundError as e:
        st.error(f"Error al cargar imagen: {str(e)}")
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
    
    st.title("SARA")
    
    # Mostrar el subtítulo en una sola línea usando HTML/CSS
    st.markdown(
        """
        <h3 style="font-size: 1.1rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
           Sistema Asistencial para Respuestas al Camino
        </h3>
        """, 
        unsafe_allow_html=True
    )

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Get LLM response with a spinner
        with st.spinner(" SARA está pensando..."):
            llm_response = send_message_to_llm(st.session_state.session_id, user_input)

        # Add LLM response to chat history
        st.session_state.messages.append({"role": "assistant", "content": llm_response})
        with st.chat_message("assistant"):
            st.write(llm_response)

if __name__ == "__main__":
    main()

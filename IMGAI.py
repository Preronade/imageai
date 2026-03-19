import streamlit as st
import os
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# --- SIMPLE LOGIN ---
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔍 IMGAI - Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "user1" and password == "mypassword156":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Wrong username or password!")
        return False
    return True

if check_login():
    st.title("🔍 IMGAI")
    st.write("Upload any image and ask questions about it!")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if not api_key:
        st.error("GROQ_API_KEY missing in .env file!")
    else:
        client = Groq(api_key=api_key)

        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])
        user_question = st.text_input("Ask something about the image:", placeholder="What is in this image?")

        if st.button("Analyze Image"):
            if not uploaded_file:
                st.warning("Please upload an image first!")
            elif not user_question:
                st.warning("Please type a question!")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
                        mime_type = uploaded_file.type

                        response = client.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": f"data:{mime_type};base64,{image_data}"
                                            }
                                        },
                                        {
                                            "type": "text",
                                            "text": user_question
                                        }
                                    ]
                                }
                            ]
                        )
                        st.success("Analysis Complete!")
                        st.write(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error: {e}")
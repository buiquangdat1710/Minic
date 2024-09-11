import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import time
import os
import streamlit.components.v1 as com

page_bg_img = '''
<style>
.stApp {
  background-image: url("https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?q=80&w=3774&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
  background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Login section
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login to Minic")
    with st.form(key='login_form'):
        username = st.text_input("Username:", key="username", help="Enter your username", placeholder="Your username")
        password = st.text_input("Key Code:", type="password", key="password", help="Enter your key code", placeholder="Key Code")
        submit_button = st.form_submit_button("Log in", help="Click to Log in")

        if submit_button:
            load_dotenv()
            key_code = os.getenv("KEY_CODE")
            if password == key_code:
                st.session_state.logged_in = True
                st.session_state.name = username
                st.success("Log in successfully!")
            else:
                st.error("Wrong key, please [contact me](https://www.facebook.com/buiquangdat2004?locale=vi_VN) to receive the key code.")
else:
    # Phần còn lại của ứng dụng sau khi đăng nhập thành công
    st.markdown(
        """
        <div style="text-align: center;">
            <h2>Minic - The Simple Chatbot</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key = api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in  st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Hãy nhập vào yêu cầu?"):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message('user'):
            st.markdown(prompt)

        with st.chat_message('assistant'):
            full_res = ""
            holder = st.empty()

            for response in client.chat.completions.create(
                model = st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_res += (response.choices[0].delta.content or "")
                holder.markdown("Minic: " + full_res + "▌")
                holder.markdown("Minic: " + full_res)
            holder.markdown("Minic: " + full_res)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_res
            }
        )

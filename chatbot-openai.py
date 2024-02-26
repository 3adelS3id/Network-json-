import openai
import streamlit as st

st.title("Chat-BOT")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.echo(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.chat_completion(
            model=st.session_state["openai_model"],
            messages=[
                 {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].message.get("content", "") 
      #     full_response = "No response from the assistant."
            message_placeholder.markdown(full_response + "")
        message_placeholder.markdown(full_response)
       # st.error(f"Response choices: {response.choices}")
    st.session_state.messages.append({"role": "assistant", "content": full_response})

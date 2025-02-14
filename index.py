import streamlit as st 
from groq import Groq



DEFAULT_MESSAGE = {
    "role": "system",
    "content": 'You are a very helpful assistant!'
}

chat_messages = [ DEFAULT_MESSAGE ]

st.set_page_config(
    page_title="ChatGPT Like",
    page_icon=":robot_face:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("Personal Assistant :rocket:")
with st.expander("Disclaimer"):
    st.write("This is for the practice purpose")

with st.sidebar:
    st.header("PantherSchools")
    groq_api_key = st.text_input("Groq API Key", type="password")
    st.logo(
        image="https://www.pantherschools.com/wp-content/uploads/2022/02/cropped-logoblack.png",
        size="large",
        link="https://www.pantherschools.com"
    )

llm = Groq(api_key=groq_api_key)

## sesstion {
#    key: value
#    key: value
# }

# Store the message in the session state
# more than message - [  ]

# One time task when the application is initialized
if "message_history" not in st.session_state:
    st.session_state.message_history = []
    st.session_state.message_history.append({
        "role": "assistant",
        "content": "How can I help you today?"
    })

# st.session_state.message_history

for message in st.session_state.message_history:
    with st.chat_message( message["role"] ):
        st.write( message["content"] )

prompt = st.chat_input("Chat with me")
if prompt:

    # check if the API Key is provided or Not
    if not groq_api_key.startswith("gsk_"):
        st.warning("Please enter your Groq API key", icon="⚠")

    if groq_api_key.startswith("gsk_"):

        with st.chat_message("user"):
            st.write(prompt)
            st.session_state.message_history.append({
                "role": "user",
                "content": prompt
            })
        chat_messages.append({
            "role": "user",
            "content": prompt
        })
        # Call groq inference to interact with LLM

        chat_completion = llm.chat.completions.create(
            messages= chat_messages,
            model="llama-3.3-70b-versatile",
            top_p=1,
            stream=False
        )
        response = chat_completion.choices[0].message.content
        with st.chat_message("assistant"):
            st.write(response)
            st.session_state.message_history.append({
                "role": "assistant",
                "content": response
            })
        chat_messages.append({
            "role": "assistant",
            "content": response
        })
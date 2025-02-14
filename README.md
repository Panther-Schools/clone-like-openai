# Clone Like OpenAI ChatGPT
This repo is just for learning purpose

![image](https://github.com/user-attachments/assets/ee06230b-a586-4978-820c-969c80ce3ff3)


# 1. Chatbot using Python, groq & streamlit
This repo contains the codebase for the chatbot application developed using Python and OPENAI

## Prerequisite
- Python, Download it from [Here](https://www.python.org/downloads/)
- anaconda, Download it from [Here](https://www.anaconda.com/download/success)
- VSCode, Download it from [Here](https://code.visualstudio.com/)
- Streamlit Document can be found [Here](https://docs.streamlit.io/develop/tutorials)

## Python library Dependency

- groq
- python-dotenv
- streamlit

## Session State in Streamlit
- a python object that exists in memory for the users/application to use

1. For the Steamlit application the sessions exist as long as the user keeps the tab open
2. OR the application maintains the active connection between the front-end and the back-end

Sessions are maintained separately for every user. For example,if user A is using the app in the USA and user B is using it in India then both sessions will not impact each other session

Session State
- Session is what happens in the browsers, the actions taken by the users
- State is how we capture that session and store the current value of the widget to use later 

Session State is like a Dictionaries({}) where we can add the key and value pair to access it later for usage purposes

## Create Virtual Environment

We are going to use Anaconda for creating the virtual environment. You can download Anaconda from here.
use the below command to create the virtual environment
```
conda create -p venv python==3.12
```
After you have created the virtual environment you need to activate the virtual environment. 
To activate the environment use the below command
```
conda activate venv
```
## Steps to run

1. Download the code using ```git clone https://github.com/Panther-Schools/clone-like-openai.git```
2. Open the cloned folder in VS Code and create the Virtual Environment using ```conda create -p venv python==3.12```
3. Activate the virtual environment using ```conda activate venv```
4. (For Mac) Install the required dependencies using ```pip install -r requirements.txt```
5. (For Windows) Install the required dependencies using ```pip3 install -r requirements.txt```
6. Run using ```streamlit run index.py or streamlit run chatgpt.py```

## Complete Code
```python

from groq import Groq
import streamlit as st
import time

SYSTEM_MESSAGE = {
    "role": "system",
    "content": "you are a helpful assistant."
}
chat_messages = [SYSTEM_MESSAGE]

st.set_page_config(
    page_title="Personal Assistant",
    page_icon=":robot_face:",
    layout="centered", 
    initial_sidebar_state="auto", 
    menu_items=None
)

st.header("Personal Assistant :rocket:")

with st.expander("Disclaimer"):
    st.write('''
        This is just for the learning purpose
    ''')

with st.sidebar:
    # new_chat = st.button(label="New Chat", type="secondary", help="Click here to start a new chat!")
    col1, col2 = st.columns(2)
    st.title("Groq API Key")
    groq_api_key = st.text_input("Groq API Key",type="password")
    with col1:
        st.logo(
            image="https://www.pantherschools.com/wp-content/uploads/2022/02/cropped-logoblack.png",
            size="large",
            link=None
        )

client = Groq(api_key= groq_api_key )

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "How can I help you today?"
    })

for history in st.session_state.messages:
    with st.chat_message(history['role']):
        st.write(history['content'])

def stream_data(chat_response):
    for word in chat_response:
        yield word
        time.sleep(0.02)

user_input = st.chat_input("Say something")
if user_input:

    if not groq_api_key.startswith("gsk_"):
        st.warning("Please enter your Groq API key!", icon="⚠")

    if groq_api_key.startswith("gsk_"):
        with st.chat_message("user"):
            st.write(user_input)
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
        chat_messages.append({
            "role": "user",
            "content": user_input
        })
        with st.chat_message("assistant"):
            chat_completion = client.chat.completions.create(
                messages=chat_messages,
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_completion_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )
            bot_response = chat_completion.choices[0].message.content
            st.session_state.messages.append({
                "role": "assistant",
                "content": bot_response
            })
            st.write( bot_response )
            # st.write_stream( stream_data(bot_response))
            st.feedback(
                "thumbs"
            )

```

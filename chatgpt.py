import streamlit as st
from datetime import datetime, timedelta
from groq import Groq
# Set page config to wide mode and add custom title
st.set_page_config(
    page_title="ChatGPT Clone",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define all functions at the top
def search_chats(query):
    results = []
    for chat_id, chat_data in st.session_state.chat_history.items():
        # Search in chat title
        if query.lower() in chat_data["title"].lower():
            results.append((chat_id, chat_data))
            continue
        
        # Search in messages
        for message in chat_data["messages"]:
            if query.lower() in message["content"].lower():
                results.append((chat_id, chat_data))
                break
    
    return results

def reset_session_state():
    st.session_state.chat_history = {}  # {chat_id: {"title": str, "messages": list, "created_at": datetime}}
    st.session_state.current_chat_id = None
    st.session_state.messages = []

def create_new_chat():
    # Check if there's an empty chat we can use
    for chat_id, chat_data in st.session_state.chat_history.items():
        if not chat_data["messages"]:
            st.session_state.current_chat_id = chat_id
            st.session_state.messages = []
            return chat_id

    # If no empty chat found, create a new one
    chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.chat_history[chat_id] = {
        "title": "New Chat",
        "messages": [],
        "created_at": datetime.now()
    }
    st.session_state.current_chat_id = chat_id
    st.session_state.messages = []
    return chat_id

# Initialize session state variables
if 'chat_history' not in st.session_state:
    reset_session_state()
    create_new_chat()  # Create initial chat
if 'current_chat_id' not in st.session_state:
    st.session_state.current_chat_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'show_search' not in st.session_state:
    st.session_state.show_search = False
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

SYSTEM_MESSAGE = {
    "role": "system",
    "content": "you are a helpful assistant."
}

chat_messages = [SYSTEM_MESSAGE]

# Ensure all chat history entries have created_at field
for chat_id, chat_data in st.session_state.chat_history.items():
    if isinstance(chat_data, dict) and 'created_at' not in chat_data:
        chat_data['created_at'] = datetime.now()
    elif not isinstance(chat_data, dict):
        # Convert old format to new format
        st.session_state.chat_history[chat_id] = {
            "title": chat_data,
            "messages": [],
            "created_at": datetime.now()
        }

def update_chat_title(chat_id, messages):
    if messages:
        for message in messages:
            if message["role"] == "user":
                title = message["content"][:30] + "..." if len(message["content"]) > 30 else message["content"]
                st.session_state.chat_history[chat_id]["title"] = title
                break

def get_categorized_chats():
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)
    week_start = today - timedelta(days=today.weekday())
    last_week_start = week_start - timedelta(days=7)

    categories = {
        "Today": [],
        "Yesterday": [],
        "This Week": [],
        "Last Week": [],
        "Older": []
    }

    for chat_id, chat_data in st.session_state.chat_history.items():
        created_at = chat_data.get("created_at", now)  # Default to now for old entries
        if created_at >= today:
            categories["Today"].append((chat_id, chat_data))
        elif created_at >= yesterday:
            categories["Yesterday"].append((chat_id, chat_data))
        elif created_at >= week_start:
            categories["This Week"].append((chat_id, chat_data))
        elif created_at >= last_week_start:
            categories["Last Week"].append((chat_id, chat_data))
        else:
            categories["Older"].append((chat_id, chat_data))

    # Sort chats within each category
    for category in categories.values():
        category.sort(key=lambda x: x[1].get('created_at', datetime.now()), reverse=True)

    return categories

# Custom CSS for styling
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #ffffff;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #f0f0f0;
    }
    .chat-message.assistant {
        background-color: #ffffff;
    }
    .chat-history-item {
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 6px;
        cursor: pointer;
        transition: background-color 0.3s;
        color: #ECECF1 !important;
    }
    .chat-history-item:hover {
        background-color: #f0f0f0;
    }
    .chat-history-item.active {
        background-color: #e6e6e6;
    }
    .user-profile {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 5px 15px;
        border-radius: 20px;
        cursor: pointer;
        position: fixed;
        right: 20px;
        top: 20px;
        background-color: white;
        z-index: 1000;
    }
    .user-menu {
        position: fixed;
        right: 20px;
        top: 60px;
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 8px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
        min-width: 150px;
    }
    .user-menu-item {
        padding: 8px 16px;
        cursor: pointer;
        color: #333;
    }
    .user-menu-item:hover {
        background-color: #f0f0f0;
    }
    .user-avatar {
        width: 35px;
        height: 35px;
        border-radius: 50%;
    }
    .chat-history-category {
        color: #666;
        font-size: 0.85em;
        font-weight: 600;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        padding-left: 12px;
        text-transform: uppercase;
    }
    .chat-history-item {
        text-align: left;
    }
    .stButton button {
        width: 100%;
        text-align: left !important;
        padding: 10px 12px;
        background-color: transparent;
        border: none;
        color: #1a1a1a;
        margin: 1px 0;
        line-height: 1.3;
        font-size: 0.95em;
        border-radius: 4px;
        min-height: 44px;
        white-space: normal !important;
        height: auto !important;
    }
    .stButton button:hover {
        background-color: rgba(0, 0, 0, 0.05) !important;
        border: none;
        color: #1a1a1a !important;
    }
    .stButton button[data-active="true"], 
    .stButton button:active {
        background-color: rgba(0, 0, 0, 0.1) !important;
    }
    .new-chat-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    .new-chat-container button {
        flex-grow: 1;
    }
    .search-button {
        padding: 8px !important;
        border-radius: 6px !important;
        min-width: 40px !important;
    }
    .search-container {
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .search-result {
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 6px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .search-result:hover {
        background-color: #2c2c2c;
        color: white;
    }
    .main-content {
        margin-top: 60px;
    }
    .logo-title {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .logo-title img {
        width: 30px;
        height: 30px;
    }
    .user-profile:hover {
        background-color: #f0f0f0;
    }
    /* Style for the sidebar */
    [data-testid="stSidebar"] {
        background-color: #f7f7f8;
    }
    
    /* Style for the new chat button */
    .new-chat-btn button {
        background-color: #ffffff !important;
        border: 1px solid #e5e5e5 !important;
        margin-bottom: 20px;
        font-weight: 500;
    }
    
    .new-chat-btn button:hover {
        background-color: #f5f5f5 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Add user menu at the top of the app
col1, col2 = st.columns([3, 1])

# Add container for main content
main_content = st.container()

with main_content:
    # Sidebar
    with st.sidebar:
        # Logo and title
        st.markdown(
            """
            <div class="logo-title">
                <img src="https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg">
                <h2>ChatGPT</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        groq_api_key = st.text_input("Groq API Key", type="password", key="groq_api_key")
        client = Groq(api_key= groq_api_key )
        # New chat and search buttons
        col1, col2 = st.columns([5, 1])
        with col1:
            with st.container():
                if st.button("+ New chat", use_container_width=True, key="new_chat_btn"):
                    new_chat_id = create_new_chat()
                    st.rerun()
        with col2:
            if st.button("🔍", key="search_btn", help="Search in chat history"):
                st.session_state.show_search = True
                st.rerun()

        # Search interface
        if st.session_state.show_search:
            search_query = st.text_input("Search chats", value=st.session_state.search_query, key="search_input")
            if search_query != st.session_state.search_query:
                st.session_state.search_query = search_query
                st.rerun()

            if search_query:
                search_results = search_chats(search_query)
                if search_results:
                    st.markdown("### Search Results")
                    for chat_id, chat_data in search_results:
                        is_active = chat_id == st.session_state.current_chat_id
                        if st.button(
                            chat_data["title"],
                            key=f"search_{chat_id}",
                            use_container_width=True,
                            type="secondary",
                            disabled=is_active,
                        ):
                            st.session_state.current_chat_id = chat_id
                            st.session_state.messages = chat_data["messages"]
                            st.rerun()
                else:
                    st.info("No results found")
            
            if st.button("Clear Search", key="clear_search"):
                st.session_state.show_search = False
                st.session_state.search_query = ""
                st.rerun()

        # Display categorized chat history
        if not st.session_state.show_search:
            categories = get_categorized_chats()
            
            for category, chats in categories.items():
                if chats:  # Only show categories that have chats
                    st.markdown(f"<div class='chat-history-category'>{category}</div>", unsafe_allow_html=True)
                    for chat_id, chat_data in chats:
                        title = chat_data["title"]
                        is_active = chat_id == st.session_state.current_chat_id
                        
                        if st.button(
                            title,
                            key=f"chat_{chat_id}",
                            use_container_width=True,
                            type="secondary",
                            disabled=is_active,
                        ):
                            st.session_state.current_chat_id = chat_id
                            st.session_state.messages = chat_data["messages"]
                            st.rerun()

# Main chat interface
if st.session_state.current_chat_id is None:
    st.markdown("# What can I help with?")
    # Create a default chat if none exists
    if not st.session_state.chat_history:
        create_new_chat()
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Message ChatGPT"):

        if not groq_api_key.startswith("gsk_"):
            st.warning("Please enter your Groq API key!", icon="⚠")

        if groq_api_key.startswith("gsk_"):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            chat_messages.append({
                "role": "user",
                "content": prompt
            })
            chat_completion = client.chat.completions.create(
                messages=chat_messages,
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_completion_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )

            st.session_state.messages.append({"role": "assistant", "content": chat_completion.choices[0].message.content})
            chat_messages.append({
                "role": "assiatant",
                "content": chat_completion.choices[0].message.content
            })
            # Update the chat history
            current_chat_id = st.session_state.current_chat_id
            st.session_state.chat_history[current_chat_id]["messages"] = st.session_state.messages
            
            # Update the chat title if it's still "New Chat"
            if st.session_state.chat_history[current_chat_id]["title"] == "New Chat":
                update_chat_title(current_chat_id, st.session_state.messages)
            
            st.rerun()
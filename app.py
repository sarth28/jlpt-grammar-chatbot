import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="JLPT Sensei", page_icon="🏮", layout="centered")

# Custom CSS for a clean look
st.markdown("""
    <style>
    .main { background-color: #fcfaf7; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #d32f2f; color: white; }
    .sensei-box { 
        padding: 20px; 
        border-radius: 15px; 
        background-color: #ffffff; 
        border-left: 5px solid #d32f2f;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🏮 JLPT Sensei AI")
st.markdown("*Japanese Grammar Tutoring*")
st.divider()

# Sidebar for Info
with st.sidebar:
    st.header("Study Stats")
    st.info("Currently learning from: **JLPT.csv**")
    st.write("Model: `llama-3.3-70b-versatile`")
    if st.button("Clear Conversation"):
        st.session_state.history = []

# State management for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User Input
with st.form(key="chat_form", clear_on_submit=True):
    user_query = st.text_input("Ask Sensei about a grammar point (e.g., 'How do I use ~ndesu?')", placeholder="Type here...")
    submit_button = st.form_submit_button(label="Ask Sensei")

if submit_button and user_query:
    with st.spinner("Sensei is thinking..."):
        try:
            # Connect to your FastAPI endpoint
            response = requests.get(f"http://127.0.0.1:8000/ask", params={"question": user_query})
            data = response.json()
            
            # Save to history
            st.session_state.history.append({"q": user_query, "a": data["sensei_says"], "src": data["source_grammar"]})
        except Exception as e:
            st.error(f"Could not connect to Sensei backend: {e}")

# Display Chat History (Newest first)
for chat in reversed(st.session_state.history):
    st.markdown(f"**You:** {chat['q']}")
    st.markdown(f"""<div class="sensei-box">
        <b>Sensei:</b><br>{chat['a']}<br><br>
        <small><i>Source Grammar: {chat['src']}</i></small>
    </div>""", unsafe_allow_html=True)
    st.write("")
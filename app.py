import streamlit as st
import pandas as pd
from datetime import datetime
import nltk
from nltk.chat.util import Chat, reflections

# Download necessary NLTK resources
nltk.download('punkt')

# Define the chatbot pairs with more diverse patterns and responses
chat_pairs = [
    (r'hi|hello|hey', ['Hello! How can I assist you today?', 'Hi there! How can I help?']),
    (r'how are you?', ['I am doing well, thank you! How can I assist you?']),
    (r'what is your name?', ['I am a chatbot built with NLTK.']),
    (r'how old are you?', ['I am just a computer program, so I don\'t have an age!']),
    (r'where are you from?', ['I was created by a programmer, so I don\'t have a physical location.']),
    (r'what can you do?', ['I can answer questions, chat with you, and provide useful information!']),
    (r'what is your favorite color?', ['I don\'t have personal preferences, but I think blue is nice!']),
    (r'what is the time?', [f'The current time is {datetime.now().strftime("%H:%M:%S")}']),
    (r'what is the date?', [f'Today is {datetime.now().strftime("%Y-%m-%d")}']),
    (r'what is the weather like?', ['Sorry, I can\'t check the weather right now. But you can use a weather app for that!']),
    (r'who created you?', ['I was created by a programmer using the NLTK library.']),
    (r'who are you?', ['I am your friendly chatbot, here to answer your questions!']),
    (r'tell me a joke', ['Why don\'t scientists trust atoms? Because they make up everything!']),
    (r'what do you do?', ['I am a chatbot created to help you with various questions and tasks.']),
    (r'(.*) nice(.*)', ['Thanks! Glad you liked it!']),
    (r'(.*) your (.*)', ['Why are you asking about my {}?', 'I am just a chatbot.']),
    (r'(.*)', ['I am sorry, I don\'t quite understand that. Could you try asking in another way?'])
]

# Initialize the chatbot with the extended pairs
chatbot = Chat(chat_pairs, reflections)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# About Section
def show_about():
    st.sidebar.title("About")
    st.sidebar.info(
        """
        **Simple NLTK Chatbot**
        This chatbot uses the NLTK library to respond to basic queries.
        Features:
        - Real-time conversation
        - Downloadable chat history
        - Persistent conversation view
        """
    )

# Function to get chatbot response using NLTK
def chatbot_response(user_input):
    return chatbot.respond(user_input)

# Function to export chat history to CSV
def export_csv(chat_data):
    df = pd.DataFrame(chat_data, columns=["Timestamp", "User", "Bot"])
    return df.to_csv(index=False).encode("utf-8")

# Streamlit Layout
st.title("Enhanced NLTK-based Chatbot")
st.subheader("Chat with me below!")

# Sidebar for About Section
show_about()

# Chat Interface
user_input = st.text_input("You:", key="user_input", placeholder="Type your message here...")

if user_input:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot_response = chatbot_response(user_input)

    # Append to conversation history
    st.session_state["chat_history"].append([timestamp, user_input, bot_response])

# Display Conversation History
st.markdown("### Conversation History")
for chat in st.session_state["chat_history"]:
    st.write(f"**You:** {chat[1]}")
    st.write(f"**Bot:** {chat[2]}")

# Export to CSV Button
if st.session_state["chat_history"]:
    st.download_button(
        label="Download Chat History as CSV",
        data=export_csv(st.session_state["chat_history"]),
        file_name="chat_history.csv",
        mime="text/csv",
    )

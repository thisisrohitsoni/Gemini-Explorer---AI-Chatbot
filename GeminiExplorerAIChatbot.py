import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel

# Set up the project
project = "gemini-explorer-433915"
vertexai.init(project=project)

# Load and start the model with configuration
config = generative_models.GenerationConfig(temperature=0.5)
model = GenerativeModel("gemini-pro", generation_config=config)
chat = model.start_chat()

# Helper function to display and send streamlit messages
def llm_function(chat, query):
    try:
        response = chat.send_message(query)
        output = response.candidates[0].content.parts[0].text
    except Exception as e:
        output = f"Error: {e}"

    # Display the model's response in Streamlit
    with st.chat_message("model"):
        st.markdown(output)

    # Append messages to session state
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "model", "content": output})

# Streamlit front-end code
st.title("Gemini AI Chatbot")

# Capture user's name for personalization
user_name = st.text_input("")

# Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Check if message history is empty and send the initial personalized message
if len(st.session_state.messages) == 0:
    if user_name:  # Personalized greeting if the user has entered their name
        initial_prompt = f"Hello, {user_name}! I'm ReX, your assistant powered by Google Gemini! 😊"
    else:  # Default introduction if the user's name is not available
        initial_prompt = "Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive."
    
    llm_function(chat, initial_prompt)

# Display and load chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture user input and process it
if query := st.chat_input("Ask something to the AI:"):
    # Display the user's message
    with st.chat_message("user"):
        st.markdown(query)

    # Process the user's query and get the model's response
    llm_function(chat, query)

# Optional: Persist chat history (consider using a database or other storage)
# Optional: Implement custom greetings or other features based on your needs
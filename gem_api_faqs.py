import streamlit as st
import csv
import requests

# Your Gemini API key
API_KEY = "Your API KEY"

# Define the personality and tone
personality = "friendly and professional"

# Load the FAQ data from CSV
faq_data = {}
with open('mental_health_faq.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        question = row['Question'].strip().lower()
        answer = row['Answer'].strip()
        faq_data[question] = answer

# Define a function to handle greetings
def handle_greeting(user_input):
    greetings = ["hello", "hi", "hey"]
    if any(greeting in user_input.lower() for greeting in greetings):
        return "Hello! How can I support you today?"
    return None

# Define a function to handle mental health-related queries
def handle_query(user_input):
    if "stress" in user_input.lower():
        return "Stress can be managed through relaxation techniques, healthy habits, and seeking support from loved ones. Would you like more information on stress management?"
    elif "anxiety" in user_input.lower():
        return "Anxiety can be challenging, but there are effective strategies and treatments available. Would you like to learn more about coping with anxiety or finding professional help?"
    elif "depression" in user_input.lower():
        return "Depression is a serious condition, and it's important to reach out for professional help if you're struggling. Would you like information on support resources or ways to talk about it?"
    return None

# Define a function to handle FAQ questions
def handle_faq(user_input):
    user_input = user_input.lower().strip()
    if user_input in faq_data:
        return faq_data[user_input]
    return None

# Define a function for fallback responses
def fallback_response():
    return "I'm here to help. If you could provide more details or ask another question, I'll do my best to assist you."

# Define the function to call the Gemini API
def call_gemini_api(user_input):
    # Replace with the actual Gemini API endpoint
    endpoint = "replace with your actual API"
    
    # Set up headers with the API key
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare the data to send to the API
    data = {
        "input": user_input,
        "personality": personality
    }
    
    # Make the POST request to the API
    response = requests.post(endpoint, headers=headers, json=data)
    
    # Check for successful response
    if response.status_code == 200:
        return response.json().get("response", "Sorry, I couldn't generate a response.")
    else:
        return f"Request failed with status code {response.status_code}: {response.text}"

# Define the chatbot function
def chatbot_response(user_input, history):
    # Add user input to history
    history.append({"role": "user", "content": user_input})
    
    # Check for greeting
    greeting_response = handle_greeting(user_input)
    if greeting_response:
        history.append({"role": "assistant", "content": greeting_response})
        return greeting_response, history
    
    # Check for specific mental health queries
    query_response = handle_query(user_input)
    if query_response:
        history.append({"role": "assistant", "content": query_response})
        return query_response, history
    
    # Check for FAQ match
    faq_response = handle_faq(user_input)
    if faq_response:
        history.append({"role": "assistant", "content": faq_response})
        return faq_response, history
    
    # Call Gemini API for a response
    bot_response = call_gemini_api(user_input)
    
    # Apply tone/personality to the response
    if personality == "friendly and professional":
        bot_response = f"🌟 {bot_response} - If you have more questions or need further assistance, I'm here to help."
    elif personality == "formal":
        bot_response = f"Thank you for your inquiry. {bot_response} Please let me know if further assistance is required."
    
    history.append({"role": "assistant", "content": bot_response})
    return bot_response, history

# Streamlit UI
st.title("Amira - Mental Health Chatbot")
st.write("Hello! I am Amira, your mental health assistant. How can I support you today?")

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        response, updated_history = chatbot_response(user_input, st.session_state.history)
        st.session_state.history = updated_history
        st.write(f"Amira: {response}")
    else:
        st.write("Amira: Please enter a message.")

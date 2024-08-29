import streamlit as st
import csv
from transformers import AutoTokenizer, AutoModelForCausalLM

# Initialize the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Set padding token
tokenizer.pad_token = tokenizer.eos_token

# Load FAQ data
faq_data = {}
with open('mental_health_faq.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        question = row['Question'].strip().lower()
        answer = row['Answer'].strip()
        faq_data[question] = answer

# Define the chatbot response function
def chatbot_response(user_input):
    user_input = user_input.lower().strip()
    if user_input in faq_data:
        return faq_data[user_input]
    inputs = tokenizer(user_input + tokenizer.eos_token, return_tensors='pt', padding=True, truncation=True)
    bot_output = model.generate(inputs['input_ids'], attention_mask=inputs['attention_mask'], max_length=1000)
    return tokenizer.decode(bot_output[0], skip_special_tokens=True)

# Streamlit UI
st.title("Amira - Mental Health Chatbot")
st.write("Hello! I am Amira, your mental health assistant. How can I help you today?")

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        response = chatbot_response(user_input)
        st.write(f"Amira: {response}")
    else:
        st.write("Amira: Please enter a message.")

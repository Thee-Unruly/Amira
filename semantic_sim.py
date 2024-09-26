import streamlit as st
import csv
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the model and tokenizer for embeddings
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")  # Sentence embedding model
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Load FAQ data from the CSV file
faq_data = {}
faq_questions = []  # Store all questions for semantic similarity calculations
with open('mental_health_faq.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        question = row['Question'].strip().lower()
        answer = row['Answer'].strip()
        faq_data[question] = answer
        faq_questions.append(question)

# Function to compute sentence embeddings using the model
def get_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state[:, 0, :]  # Extract embeddings from the [CLS] token
    return embeddings

# Define the chatbot's response logic
def chatbot_response(user_input):
    # Preprocess the user input
    user_input = user_input.lower().strip()
    
    # Compute embeddings for the user's input
    user_embedding = get_embeddings(user_input)

    # Compute embeddings for all FAQ questions
    faq_embeddings = get_embeddings(faq_questions)

    # Calculate cosine similarity between user input and each FAQ question
    similarities = cosine_similarity(user_embedding.numpy(), faq_embeddings.numpy())[0]
    
    # Identify the most similar question based on similarity scores
    best_match_index = similarities.argmax()
    best_match_score = similarities[best_match_index]

    # Return the answer if the similarity score exceeds the threshold
    if best_match_score > 0.7:
        matched_question = faq_questions[best_match_index]
        return faq_data[matched_question]
    
    # If no sufficiently similar match is found, generate a custom response
    inputs = tokenizer(user_input + tokenizer.eos_token, return_tensors='pt', padding=True, truncation=True)
    generated_output = model.generate(inputs['input_ids'], attention_mask=inputs['attention_mask'], max_length=1000)
    return tokenizer.decode(generated_output[0], skip_special_tokens=True)

# Streamlit UI setup
st.title("Amira - Mental Health Chatbot")
st.write("Hello! I am Amira, your mental health assistant. How can I help you today?")

# Accept user input
user_input = st.text_input("You:", "")

# Handle button click for generating a response
if st.button("Send"):
    if user_input:
        response = chatbot_response(user_input)
        st.markdown(f"**Amira:** {response}")
    else:
        st.write("Amira: Please enter your message.")

import csv
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

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
        return "Hello! How can I assist you today?"
    return None

# Define a function to handle queries
def handle_query(user_input):
    if "product" in user_input.lower():
        return "We offer a variety of products. Can you specify which product you are interested in?"
    elif "order" in user_input.lower():
        return "I can help you with order status. Please provide your order number."
    return None

# Define a function to handle FAQ questions
def handle_faq(user_input):
    user_input = user_input.lower().strip()
    if user_input in faq_data:
        return faq_data[user_input]
    return None

# Define a function for fallback responses
def fallback_response():
    return "I'm not sure I understand. Could you please provide more details or ask something else?"

# Define the chatbot function
def chatbot_response(user_input):
    # Check for greeting
    greeting_response = handle_greeting(user_input)
    if greeting_response:
        return greeting_response
    
    # Check for specific queries
    query_response = handle_query(user_input)
    if query_response:
        return query_response
    
    # Check for FAQ match
    faq_response = handle_faq(user_input)
    if faq_response:
        return faq_response
    
    # Generate a response using the model if no specific handling was done
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    bot_output = model.generate(new_user_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    bot_response = tokenizer.decode(bot_output[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    # Apply tone/personality to the response
    if personality == "friendly and professional":
        bot_response = f"😊 {bot_response} - Let me know if there's anything else I can help with!"
    elif personality == "formal":
        bot_response = f"Thank you for your inquiry. {bot_response} Please let me know if further assistance is required."
    
    return bot_response

# Example interaction
user_input = input("You: ")
print("Amira:", chatbot_response(user_input))

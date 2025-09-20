# 1. Import all necessary libraries
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 2. Securely load your API key from the .env file
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

# Check to make sure the key loaded correctly
if not api_key:
    raise ValueError("API Key not found. Please check your .env file.")

# 3. Configure the Gemini API client
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Initialize the chat session with a starting prompt
# This sets the persona for the entire conversation.
chat = model.start_chat(history=[
    {"role": "user", "parts": [
        "You are a helpful Socratic tutor for computer science students. "
        "Your purpose is to guide them to the correct answer by asking clarifying questions, "
        "not by giving them the solution."
    ]}
])

# 5. Start a continuous loop for the conversation
print("Welcome to Mentor AI! Ask me a computer science question, or type 'quit' to exit.")

while True:
    # Get user input from the terminal
    user_input = input("You: ")
    
    # Check if the user wants to quit
    if user_input.lower() in ["quit", "exit"]:
        print("Goodbye!")
        break
    
    try:
        # Send the user's message to the chat session
        response = chat.send_message(user_input)
        
        # Print the AI's response
        print("Mentor AI:", response.text)

    except Exception as e:
        print(f"An error occurred: {e}")
# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. API Configuration: Your AI key and model setup
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API Key not found. Please check your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. FastAPI Setup: Create the application instance
app = FastAPI()

# 3. CORS Middleware: This allows your website to access the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Global Chat Session: This variable will store the conversation.
# It is created only once when the server starts.
chat_session = model.start_chat(history=[
    {"role": "user", "parts": [
        "You are a helpful Socratic tutor for computer science students. "
        "Your purpose is to guide them to the correct answer by asking clarifying questions, "
        "not by giving them the solution."
    ]}
])

# 5. Input Model: This ensures the data you receive from the website is correct.
class UserMessage(BaseModel):
    message: str

# 6. New API Endpoint: This is the URL the website will send messages to.
@app.post("/chat")
async def get_chat_response(input: UserMessage):
    try:
        # Use the persistent chat_session to send the user's message
        response = chat_session.send_message(input.message)

        # Return the AI's response to the website
        return {"response": response.text}

    except Exception as e:
        return {"response": f"An error occurred: {e}"}
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

# Check to make sure the key loaded correctly
if not api_key:
    raise ValueError("API Key not found. Please check your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. FastAPI Setup: Create the application instance
app = FastAPI()

# 3. CORS Middleware: This is crucial for linking your website and API.
# It allows your website (from one address) to talk to your API (at another address).
# WARNING: For production, do not use ["*"]. Replace it with your website's URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Input Model: This ensures the data you receive from the website is correct.
class UserInput(BaseModel):
    user_problem: str
    user_code: str

# 5. API Endpoint: This is the URL the website will send data to.
@app.post("/mentor")
async def get_mentor_response(input: UserInput):
    # This is the prompt that defines your AI's persona
    system_prompt = (
        "You are a helpful Socratic tutor for computer science students. "
        "Your purpose is to guide them to the correct answer by asking clarifying questions, "
        "not by giving them the solution."
    )

    # 6. AI Interaction: Send the message to the AI and get a response
    try:
        chat = model.start_chat(history=[{"role": "user", "parts": [system_prompt]}])
        response = chat.send_message(
            f"Code: `{input.user_code}`\nProblem: {input.user_problem}"
        )
        # 7. Return the response to the website
        return {"response": response.text}

    except Exception as e:
        return {"response": f"An error occurred: {e}"}
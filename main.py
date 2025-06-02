import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional, Dict

# Load environment variables
load_dotenv()

# Get the Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Initialize the Gemini model
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Welcome the user like Jarvis
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="""
# 🤖 Welcome, Commander.
I'm **Jarvis**, your AI assistant.

Type your query and let me assist you intelligently.
"""
    ).send()

# Handle user messages
@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    # Prepare conversation for Gemini
    formatted_history = [
        {"role": msg["role"] if msg["role"] == "user" else "model", "parts": [{"text": msg["content"]}]}
        for msg in history
    ]

    # Get response from Gemini
    response = model.generate_content(formatted_history)
    response_text = response.text if hasattr(response, "text") else "I'm sorry, I couldn't generate a response."

    # Save and display response
    history.append({"role": "assistant", "content": response_text})
    cl.user_session.set("history", history)

    await cl.Message(
        content=f"""
### 🤖 Jarvis:
{response_text}
"""
    ).send()

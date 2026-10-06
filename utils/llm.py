import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-3.8-flash")


def ask_ai(system_prompt: str, user_prompt: str) -> str:
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    response = model.generate_content(full_prompt)
    return response.text
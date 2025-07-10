from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

# Inicjalizacja API
app = FastAPI()

# Zezwól na połączenia z Fluttera
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ustaw klucz API z Rendera
openai.api_key = os.getenv("OPENAI_API_KEY")

# Historia rozmowy (przechowywana tymczasowo w pamięci)
chat_history = []

@app.get("/")
def root():
    return {"message": "english-ai-backend działa!"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")

    # Dodaj wiadomość użytkownika do historii
    chat_history.append({"role": "user", "content": user_message})

    # Wyślij całą historię do OpenAI
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )

    # Odpowiedź asystenta
    assistant_reply = response.choices[0].message.content

    # Zapisz odpowiedź do historii
    chat_history.append({"role": "assistant", "content": assistant_reply})

    return {"reply": assistant_reply}


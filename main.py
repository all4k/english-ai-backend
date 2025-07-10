from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Ustawienie CORS – umożliwia komunikację z Flutterem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ustaw swój klucz OpenAI (dodamy przez zmienne środowiskowe w Aptible)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    if not user_input:
        return {"error": "Brak wiadomości od użytkownika"}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś pomocnym nauczycielem angielskiego. Odpowiadaj krótko i prostym językiem."},
                {"role": "user", "content": user_input},
            ]
        )
        answer = response.choices[0].message.content.strip()
        return {"reply": answer}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "english-ai-backend działa!"}

async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")

    if not message:
        return {"error": "No message provided."}

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # możesz zmienić na gpt-4 jeśli chcesz
        messages=[
            {"role": "system", "content": "You are a helpful English teacher."},
            {"role": "user", "content": message},
        ],
        max_tokens=200,
        temperature=0.7
    )

    reply = response['choices'][0]['message']['content']
    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)


# main.py
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

chat_memory = {}

# Zet je OpenAI API key
# 1️⃣ Maak een FastAPI app aan

openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

# 2️⃣ CORS instellen
# Dit zorgt ervoor dat je frontend (website) requests kan doen naar de backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" betekent alle websites mogen connecten (voor testen)
    allow_methods=["*"],   # GET, POST etc.
    allow_headers=["*"],   # Alle headers zijn toegestaan
)

# 3️⃣ Static files mounten (JS bestanden)
# Alle bestanden in de "static" map kunnen vanaf /static/ URL benaderd worden
app.mount("/static", StaticFiles(directory="static"), name="static")

# 4️⃣ Endpoint om de website te serveren
@app.get("/")
def index():
    # Als iemand naar http://localhost:8000 gaat, geven we index.html terug
    return FileResponse("index.html")

SYSTEM_PROMPT =  """
Je bent AI-Migo, een Nederlandse AI-chatbot voor bedrijven.

Je bent:
- vriendelijk
- professioneel
- duidelijk
- kort en to-the-point

Je helpt websitebezoekers met vragen.
Je verzint nooit informatie.
Als je iets niet weet, zeg je dat eerlijk.

Als iemand vraagt wat AI-Migo is:
Leg kort uit dat AI-Migo AI-chatbots bouwt voor websites.
"""

AI_MIGO_KENNIS = """
AI-Migo helpt bedrijven met:
- AI chatbots voor websites
- Automatisering van klantenservice
- Lead generatie via chat
- 24/7 bereikbaarheid

AI-Migo richt zich op Nederlandse bedrijven.
"""

# 5️⃣ Eenvoudig chat endpoint
@app.get("/chat")
def chat(message: str, session_id: str):
    try:
        if session_id not in chat_memory:
            chat_memory[session_id] = []

        # Voeg nieuwe user message toe
        chat_memory[session_id].append(
            {"role": "user", "content": message}
        )

        # Bouw volledige message history
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": AI_MIGO_KENNIS}
        ] + chat_memory[session_id]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200
        )

        answer = response["choices"][0]["message"]["content"]

        # Sla AI antwoord ook op
        chat_memory[session_id].append(
            {"role": "assistant", "content": answer}
        )

        return {"response": answer}

    except Exception as e:
        return {"response": "Er ging iets mis: " + str(e)}


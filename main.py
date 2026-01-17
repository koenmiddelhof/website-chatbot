# main.py
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

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

# 5️⃣ Eenvoudig chat endpoint
@app.get("/chat")
def chat(message: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # of gpt-4 als je toegang hebt
            messages=[{"role": "user", "content": message}],
            max_tokens=150
        )
        answer = response['choices'][0]['message']['content']
        return {"response": answer}
    except Exception as e:
        return {"response": "Er ging iets mis met de AI: " + str(e)}


# main.py
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# 1️⃣ Maak een FastAPI app aan
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
    # Voor nu sturen we gewoon een fake antwoord terug
    return {"response": f"Je zei: {message}"}

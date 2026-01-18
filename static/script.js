// Elementen ophalen
const chatIcon = document.getElementById("chat-icon");
const chatBox = document.getElementById("chat-box");
const messages = document.getElementById("messages");
const userInput = document.getElementById("user-input");

// Chat-icoon togglen
chatIcon.onclick = () => {
    chatBox.style.display = chatBox.style.display === "none" ? "flex" : "none";
};

// 🌟 Session ID aanmaken of ophalen
let sessionId = localStorage.getItem("session_id");
if (!sessionId) {
    sessionId = crypto.randomUUID(); // unieker ID voor elke gebruiker
    localStorage.setItem("session_id", sessionId);
}

// Bericht versturen naar backend
async function sendMessage() {
    const message = userInput.value;
    if (!message) return;

    // Toon gebruikersbericht
    const userMsg = document.createElement("div");
    userMsg.textContent = "Jij: " + message;
    messages.appendChild(userMsg);

    userInput.value = "";

    try {
        // Verstuur naar backend met session_id
        const response = await fetch(`/chat?message=${encodeURIComponent(message)}&session_id=${sessionId}`);
        const data = await response.json();

        // Toon bot antwoord
        const aiMsg = document.createElement("div");
        aiMsg.textContent = "Bot: " + data.response;
        messages.appendChild(aiMsg);

        // Scroll naar beneden
        messages.scrollTop = messages.scrollHeight;
    } catch (err) {
        const errorMsg = document.createElement("div");
        errorMsg.textContent = "Bot: Er ging iets mis met de verbinding.";
        messages.appendChild(errorMsg);
    }
}


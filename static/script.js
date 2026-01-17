// Elementen ophalen
const chatIcon = document.getElementById("chat-icon");
const chatBox = document.getElementById("chat-box");
const messages = document.getElementById("messages");
const userInput = document.getElementById("user-input");

// Chat-icoon togglen
chatIcon.onclick = () => {
    chatBox.style.display = chatBox.style.display === "none" ? "flex" : "none";
};

// Bericht versturen naar backend
async function sendMessage() {
    const message = userInput.value;
    if (!message) return;

    // Toon gebruikersbericht
    const userMsg = document.createElement("div");
    userMsg.textContent = "Jij: " + message;
    messages.appendChild(userMsg);

    userInput.value = "";

    // Verstuur naar backend
    const response = await fetch(`/chat?message=${encodeURIComponent(message)}`);
    const data = await response.json();

    // Toon bot antwoord
    const aiMsg = document.createElement("div");
    aiMsg.textContent = "Bot: " + data.response;
    messages.appendChild(aiMsg);

    messages.scrollTop = messages.scrollHeight;
}

// Elementen ophalen
const chatIcon = document.getElementById("chat-icon");
const chatBox = document.getElementById("chat-box");
const chatClose = document.getElementById("chat-close");
const messages = document.getElementById("messages");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Beginstand chatbox
chatBox.style.display = "none";

// Toggle chatbox
chatIcon.onclick = () => {
    chatBox.style.display = chatBox.style.display === "none" ? "flex" : "none";
};
chatClose.onclick = () => { chatBox.style.display = "none"; };

// Session ID voor memory
let sessionId = localStorage.getItem("session_id");
if(!sessionId){
    sessionId = crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
}

// Typing indicator
function showTyping(){
    const typingWrapper = document.createElement("div");
    typingWrapper.id = "typing";
    typingWrapper.className = "message-wrapper bot";

    const avatar = document.createElement("img");
    avatar.src = "https://i.imgur.com/8Km9tLL.png"; // bot avatar
    avatar.className = "avatar";

    const dots = document.createElement("div");
    dots.className = "typing-dots";
    dots.innerHTML = "<span></span><span></span><span></span>";

    typingWrapper.appendChild(avatar);
    typingWrapper.appendChild(dots);
    messages.appendChild(typingWrapper);
    messages.scrollTop = messages.scrollHeight;
}

function hideTyping(){
    const typing = document.getElementById("typing");
    if(typing) typing.remove();
}

// Verstuur bericht
async function sendMessage(){
    const message = userInput.value;
    if(!message) return;

    // User bubble
    const wrapper = document.createElement("div");
    wrapper.className = "message-wrapper user";

    const bubble = document.createElement("div");
    bubble.className = "user";
    bubble.textContent = message;

    wrapper.appendChild(bubble);
    messages.appendChild(wrapper);
    userInput.value = "";
    showTyping();

    try{
        const res = await fetch(`/chat?message=${encodeURIComponent(message)}&session_id=${sessionId}`);
        const data = await res.json();
        hideTyping();

        const botWrapper = document.createElement("div");
        botWrapper.className = "message-wrapper bot";

        const botAvatar = document.createElement("img");
        botAvatar.src = "https://i.imgur.com/8Km9tLL.png";
        botAvatar.className = "avatar";

        const botBubble = document.createElement("div");
        botBubble.className = "bot";
        botBubble.textContent = data.response;

        botWrapper.appendChild(botAvatar);
        botWrapper.appendChild(botBubble);
        messages.appendChild(botWrapper);
        messages.scrollTop = messages.scrollHeight;

    } catch {
        hideTyping();
        const errWrapper = document.createElement("div");
        errWrapper.className = "message-wrapper bot";
        const botAvatar = document.createElement("img");
        botAvatar.src = "https://i.imgur.com/8Km9tLL.png";
        botAvatar.className = "avatar";
        const botBubble = document.createElement("div");
        botBubble.className = "bot";
        botBubble.textContent = "Er ging iets mis met de verbinding.";
        errWrapper.appendChild(botAvatar);
        errWrapper.appendChild(botBubble);
        messages.appendChild(errWrapper);
    }
}

// Event listeners
sendBtn.onclick = sendMessage;
userInput.addEventListener("keypress", function(e){
    if(e.key === "Enter") sendMessage();
});

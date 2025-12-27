const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");

/* ---------- Message helpers ---------- */

function createMessageRow(side, bubbleEl, avatarEmoji) {
    const row = document.createElement("div");
    row.className = `msg-row ${side}-row`;

    const avatar = document.createElement("div");
    avatar.className = `avatar ${side}`;
    avatar.textContent = avatarEmoji;

    if (side === "bot") {
        row.appendChild(avatar);
        row.appendChild(bubbleEl);
    } else {
        row.appendChild(bubbleEl);
        row.appendChild(avatar);
    }
    return row;
}

function addUserMessage(text) {
    const bubble = document.createElement("div");
    bubble.classList.add("message", "user");
    bubble.innerText = text;

    const row = createMessageRow("user", bubble, "👤");
    chatBox.appendChild(row);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* ---------- Typing indicator ---------- */

let typingRow = null;

function showTyping() {
    const bubble = document.createElement("div");
    bubble.className = "typing-bubble";
    bubble.innerHTML = `<span class="dot"></span><span class="dot"></span><span class="dot"></span>`;
    typingRow = createMessageRow("bot", bubble, "🤖");
    chatBox.appendChild(typingRow);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function hideTyping() {
    if (typingRow) typingRow.remove();
    typingRow = null;
}

/* ---------- Bot typing animation ---------- */

function typeBotMessage(text) {
    const bubble = document.createElement("div");
    bubble.classList.add("message", "bot");
    bubble.innerText = "";

    const row = createMessageRow("bot", bubble, "🤖");
    chatBox.appendChild(row);

    let i = 0;
    const speed = 18;

    const interval = setInterval(() => {
        bubble.innerText += text[i];
        i++;
        chatBox.scrollTop = chatBox.scrollHeight;
        if (i >= text.length) clearInterval(interval);
    }, speed);
}

/* ---------- Send message ---------- */

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addUserMessage(text);
    userInput.value = "";

    showTyping();

    try {
        const response = await fetch("http://127.0.0.1:8000/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        hideTyping();
        typeBotMessage(data.translation ?? "…");
    } catch {
        hideTyping();
        typeBotMessage("Error connecting to server.");
    }
}

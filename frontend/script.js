const API_BASE = window.location.port === "8000" ? "" : "http://127.0.0.1:8000";

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("sendBtn");

const USER_AVATAR = "You".slice(0, 1);
const BOT_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="12" rx="3"/><path d="M12 8V4M8 4h8"/><circle cx="9" cy="14" r="1"/><circle cx="15" cy="14" r="1"/></svg>';

/* ---------- Status ---------- */

async function checkHealth() {
    const badge = document.getElementById("statusBadge");
    try {
        const res = await fetch(`${API_BASE}/health`);
        const data = await res.json();
        if (data.model_ready) {
            badge.className = "status-badge online";
            badge.innerHTML = "<i></i>Model ready";
        } else {
            badge.className = "status-badge offline";
            badge.innerHTML = "<i></i>Model not loaded";
        }
    } catch {
        badge.className = "status-badge offline";
        badge.innerHTML = "<i></i>API offline";
    }
}

/* ---------- Message helpers ---------- */

function removeWelcome() {
    const w = document.getElementById("welcome");
    if (w) w.remove();
}

function createMessageRow(side, bubbleEl) {
    const row = document.createElement("div");
    row.className = `msg-row ${side}-row`;

    const avatar = document.createElement("div");
    avatar.className = `avatar ${side}`;
    if (side === "bot") avatar.innerHTML = BOT_SVG;
    else avatar.textContent = USER_AVATAR;

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
    chatBox.appendChild(createMessageRow("user", bubble));
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* ---------- Typing indicator ---------- */

let typingRow = null;

function showTyping() {
    const bubble = document.createElement("div");
    bubble.className = "typing-bubble";
    bubble.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
    typingRow = createMessageRow("bot", bubble);
    chatBox.appendChild(typingRow);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function hideTyping() {
    if (typingRow) typingRow.remove();
    typingRow = null;
}

/* ---------- Bot message with typing animation ---------- */

function typeBotMessage(text, isError = false) {
    const bubble = document.createElement("div");
    bubble.classList.add("message", "bot");
    if (isError) bubble.classList.add("error");
    else bubble.innerHTML = '<span class="lang-tag">FRANÇAIS</span>';

    const span = document.createElement("span");
    bubble.appendChild(span);
    chatBox.appendChild(createMessageRow("bot", bubble));

    let i = 0;
    const interval = setInterval(() => {
        span.innerText += text[i];
        i++;
        chatBox.scrollTop = chatBox.scrollHeight;
        if (i >= text.length) clearInterval(interval);
    }, 16);
}

/* ---------- Send ---------- */

userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text || sendBtn.disabled) return;

    removeWelcome();
    addUserMessage(text);
    userInput.value = "";
    sendBtn.disabled = true;
    showTyping();

    try {
        const response = await fetch(`${API_BASE}/translate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text }),
        });

        hideTyping();
        if (response.ok) {
            const data = await response.json();
            typeBotMessage(data.translation || "…");
        } else {
            const err = await response.json().catch(() => ({}));
            typeBotMessage(err.detail || `Request failed (${response.status})`, true);
        }
    } catch {
        hideTyping();
        typeBotMessage("Cannot reach the translation API. Is the backend running on port 8000?", true);
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

window.addEventListener("load", checkHealth);

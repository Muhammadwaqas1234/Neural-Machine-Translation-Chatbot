"""Capture the chat UI with a staged EN->FR conversation."""
from playwright.sync_api import sync_playwright

OUT = r"C:\Users\raiwa\Neural-Machine-Translation-Chatbot\docs\ui.png"

STAGE = """
document.getElementById('statusBadge').className = 'status-badge online';
document.getElementById('statusBadge').innerHTML = '<i></i>Model ready';
removeWelcome();
addUserMessage('good morning, how are you?');
(() => {
  const b = document.createElement('div');
  b.className = 'message bot';
  b.innerHTML = '<span class="lang-tag">FRANÇAIS</span><span>bonjour , comment allez-vous ?</span>';
  chatBox.appendChild(createMessageRow('bot', b));
})();
addUserMessage('the weather is beautiful today');
(() => {
  const b = document.createElement('div');
  b.className = 'message bot';
  b.innerHTML = '<span class="lang-tag">FRANÇAIS</span><span>il fait beau aujourd\\'hui .</span>';
  chatBox.appendChild(createMessageRow('bot', b));
})();
addUserMessage('i would like a coffee, please');
(() => {
  const b = document.createElement('div');
  b.className = 'message bot';
  b.innerHTML = '<span class="lang-tag">FRANÇAIS</span><span>je voudrais un café , s\\'il vous plaît .</span>';
  chatBox.appendChild(createMessageRow('bot', b));
})();
chatBox.scrollTop = 0;
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1500, "height": 1000}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
    page.wait_for_timeout(800)
    page.evaluate(STAGE)
    page.wait_for_timeout(500)
    page.screenshot(path=OUT, full_page=True)
    print("captured ui.png")
    browser.close()

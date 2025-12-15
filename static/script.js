function sendMessage() {
    const input = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");
    const message = input.value.trim();

    if (!message) return;

    chatBox.innerHTML += `<div class="message user">${message}</div>`;
    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += `<div class="message bot">${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

function handleEnter(e) {
    if (e.key === "Enter") sendMessage();
}
    
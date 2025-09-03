let lastMessageId = window.lastMessageId || 0;
const chatBox = document.getElementById("chat-box");

document.getElementById("chat-form").addEventListener("submit", async function(e) {
	e.preventDefault();
	const input = document.getElementById("msg-input");
	const content = input.value.trim();
	if (!content) return;

	const response = await fetch(`/chat/${window.chatUserId}/send`, {
		method: "POST",
		headers: { "Content-Type": "application/x-www-form-urlencoded" },
		body: new URLSearchParams({ content })
	});

	if (response.ok) {
		input.value = "";
		chatBox.scrollTop = chatBox.scrollHeight;
	}
});

async function pollUpdates() {
	try {
		const response = await fetch(`/updates?last_message_id=${lastMessageId}&timeout=25`, {
			headers: { "Accept": "application/json" }
		});

		if (response.ok) {
			const newMessages = await response.json();
			for (const msg of newMessages) {
				appendMessage(msg.sender_id, msg.content, msg.created_at);
				lastMessageId = Math.max(lastMessageId, msg.id);
			}
			chatBox.scrollTop = chatBox.scrollHeight;
		}
	} catch (err) {}
	setTimeout(pollUpdates, 1000);
}

function appendMessage(sender, content, createdAt) {
	const p = document.createElement("p");
	p.innerHTML = `<strong>${sender}:</strong> ${content} <small>${createdAt}</small>`;
	chatBox.appendChild(p);
}

pollUpdates();

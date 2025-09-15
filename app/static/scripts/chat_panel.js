let lastMessageId = 0;
let currentUserId = null;
let chatList = [];

const chatBox = document.getElementById("chat-box");
const chatUsername = document.getElementById("active-chat-name");
const chatForm = document.getElementById("chat-form");
const msgInput = document.getElementById("msg-input");
const chatContainer = document.getElementById("chat-container");

let currentOffset = 0;
const limit = 50;

function createMessageBlock(msg, incoming) {

	const wrapper = document.createElement("div");
	wrapper.className = incoming ? "message incoming" : "message own";

	const text = document.createElement("div");
	text.className = "text-content";
	text.innerHTML = msg.content;

	const time = document.createElement("span");
	time.className = "message-time";
	time.textContent = new Date(msg.created_at).toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" });

	text.appendChild(time);
	wrapper.appendChild(text);

	return wrapper;
}

function appendMessage(msg, incoming) {
	const mes_block = createMessageBlock(msg, incoming)
	chatBox.appendChild(mes_block);
	chatBox.scrollTop = chatBox.scrollHeight;
}

function prependMessage(msg, incoming) {
	const mes_block = createMessageBlock(msg, incoming)
	chatBox.prepend(mes_block);
}

async function loadMessages(userId, offset = 0, append = false) {
	const res = await fetch(`/chat/${userId}?offset=${offset}&limit=${limit}`);
	if (!res.ok) return;

	const object = await res.json();

	await console.log(object);

	const oldScrollHeight = chatBox.scrollHeight;

	object.forEach(msg => {
		if (append) {
			prependMessage(msg, msg.sender.id == currentUserId);
		} else {
			appendMessage(msg, msg.sender.id == currentUserId);
		}
		lastMessageId = Math.max(lastMessageId, msg.id);
	});

	if (append) {
		chatBox.scrollTop = chatBox.scrollHeight - oldScrollHeight;
	}
}

async function openChat(userId, username = "*NO_NAME_") {
	currentUserId = userId;
	currentOffset = 0;
	chatContainer.style = "";
	if (chatUsername) chatUsername.textContent = username;

	chatBox.innerHTML = "";
	await loadMessages(currentUserId, currentOffset, false);
	chatBox.scrollTop = chatBox.scrollHeight;
}

chatBox.addEventListener("scroll", async () => {
	if (chatBox.scrollTop === 0 && currentUserId) {
		currentOffset += limit;
		await loadMessages(currentUserId, currentOffset, true);
	}
});

async function updateChatList() {
	const res = await fetch(`/chats/list`);

	if (res.ok) {
		const object = await res.json();
		chatList = object.sort(
			(a, b) =>
				new Date(b.last_message.created_at) - new Date(a.last_message.created_at)
		);
		lastMessageId = chatList[0].last_message.id;
	}
}


function showChatList() {
	chatListObject.innerHTML = "";
	chatList.forEach(user => {
		const userDiv = document.createElement("div");
		userDiv.className = "user-list-element";
		userDiv.setAttribute("data-user-id", user.id);

		const infoDiv = document.createElement("div");
		infoDiv.className = "info";

		const titleDiv = document.createElement("div");
		titleDiv.className = "title";
		const h3 = document.createElement("h3");
		h3.className = "fullName";
		h3.textContent = user.username;
		titleDiv.appendChild(h3);

		const subtitleDiv = document.createElement("div");
		subtitleDiv.className = "subtitle";
		const subtitleP = document.createElement("p");
		subtitleP.className = "last-message";
		subtitleP.textContent = `${user.username}: ${user.last_message.content}`;
		subtitleDiv.appendChild(subtitleP);

		infoDiv.appendChild(titleDiv);
		infoDiv.appendChild(subtitleDiv);

		const infoTimeDiv = document.createElement("div");
		infoTimeDiv.className = "info-time";
		const messageTimeDiv = document.createElement("div");
		const messageTimeP = document.createElement("p")
		const createdAt = new Date(user.last_message.created_at);
		const now = new Date();

		const diffMs = now - createdAt;
		const diffHours = diffMs / (1000 * 60 * 60);

		let formattedTime;
		if (diffHours < 24) {
			formattedTime = createdAt.toLocaleTimeString("ru-RU", {
				hour: "2-digit",
				minute: "2-digit"
			});
		} else {
			formattedTime = createdAt.toLocaleDateString("ru-RU", {
				day: "2-digit",
				month: "2-digit",
				year: "2-digit"
			});
		}

		messageTimeP.textContent = formattedTime;

		messageTimeDiv.appendChild(messageTimeP);
		infoTimeDiv.appendChild(messageTimeDiv);

		userDiv.appendChild(infoDiv);
		userDiv.appendChild(infoTimeDiv);

		userDiv.addEventListener("click", () => {
			openChat(user.id, user.username)
		});
		chatListObject.appendChild(userDiv);
	});
}



document.querySelectorAll(".user-list-element").forEach(el => {
	el.addEventListener("click", () => {
		const userId = el.dataset.userId;
		const username = el.querySelector(".fullName").textContent;
		openChat(userId, username);
	});
});

chatForm.addEventListener("submit", async e => {
	e.preventDefault();
	const content = msgInput.innerText.trim();
	if (!content || !currentUserId) return;

	const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");

	const response = await fetch(`/chat/${currentUserId}/send`, {
		method: "POST",
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
			"X-CSRF-Token": csrfToken
		},
		body: new URLSearchParams({ content })
	});

	if (response.ok) {
		msgInput.innerText = "";
		msgInput.style.height = "40px";
	}
});

msgInput.addEventListener("keydown", (e) => {
	if (e.key === "Enter" && !e.shiftKey) {
		e.preventDefault();
		chatForm.requestSubmit();
	}
});

function autoResize() {
	msgInput.style.height = "auto";
	msgInput.style.height = msgInput.scrollHeight + "px";
}
msgInput.addEventListener("input", autoResize);

const userMenuToggle = document.querySelector('.user-menu-toggle');
const userMenuContainer = document.querySelector('.user-menu-container');

userMenuToggle.addEventListener('click', (e) => {
	e.stopPropagation();
	userMenuToggle.classList.toggle('active');
	userMenuContainer.classList.toggle('show');
});

document.addEventListener('click', (e) => {
	if (!userMenuContainer.contains(e.target)) {
		userMenuToggle.classList.remove('active');
		userMenuContainer.classList.remove('show');
	}
});

// WEBSOCKET

async function wsListen() {
	const res = await fetch("/ws_url");
	if (!res.ok) return;
	const { ws_url } = await res.json();

	const ws = new WebSocket(ws_url);

	ws.onopen = () => {
		console.log("Connected to WebSocket");
		ws.send(JSON.stringify({type: "ping"}));
	};

	ws.onmessage = async (event) => {
		try {
			const msg = JSON.parse(event.data);
	
			await updateChatList();  // <- надо await, иначе showChatList может сработать до fetch
			showChatList();
	
			if (msg.receiver.id != currentUserId && msg.sender.id != currentUserId) {
				return;
			}
	
			appendMessage(msg, msg.sender.id === currentUserId);
	
			lastMessageId = Math.max(lastMessageId, msg.id);
	
		} catch (err) {
			console.error("Error parsing WS message:", err);
		}
	};

	ws.onerror = (err) => {
		console.error("WebSocket error:", err);
	};

	ws.onclose = (event) => {
		console.log(`WebSocket closed: code=${event.code}, reason=${event.reason}`);
		setTimeout(wsListen, 1000);
	};
}


async function pollUpdates() {
	try {

		const res = await fetch(`/updates?last_message_id=${lastMessageId}`, {
			headers: { Accept: "application/json" }
		});
		if (res.ok) {
			const newMessages = await res.json();
			for (const msg of newMessages) {
				await updateChatList();
				showChatList();
			
				if (msg.receiver.id != currentUserId && msg.sender.id != currentUserId) {
					continue;
				}
				
				appendMessage(msg, msg.sender.id == currentUserId);
				lastMessageId = Math.max(lastMessageId, msg.id);
			}
		}
	} catch (err) {
		console.error("Error fetching updates:", err);
	}
	setTimeout(pollUpdates, 1000);
}

window.onload = async () => {
	//pollUpdates();
	wsListen();
	await updateChatList();
	showChatList();
}

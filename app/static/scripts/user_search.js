const userSearchResults = document.getElementById("userSearchResults");
const chatListObject = document.querySelector(".chat-list");
let debounceTimer = null;

async function search_users(username) {
	const response = await fetch(`/search?username=${encodeURIComponent(username)}`, {
		method: "GET",
		headers: { "Content-Type": "application/x-www-form-urlencoded" }
	});
	return await response.json();
}

document.getElementById("user_search_input").addEventListener("input", function(event) {
	const current_input = event.target.value;

	if (debounceTimer) clearTimeout(debounceTimer);

	debounceTimer = setTimeout(async () => {
		if (!current_input.trim()) {
			userSearchResults.innerHTML = "";
			chatListObject.style.display = "flex";
			return;
		}

		const users = await search_users(current_input);
		userSearchResults.innerHTML = "";
		chatListObject.style.display = "none";

		users.forEach(user => {
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
			const p = document.createElement("p");
			p.className = "last-message";
			p.textContent = "";
			subtitleDiv.appendChild(p);

			infoDiv.appendChild(titleDiv);
			infoDiv.appendChild(subtitleDiv);
			userDiv.appendChild(infoDiv);

			userDiv.addEventListener("click", () => {
				openChat(user.id, "TEST")
			});

			userSearchResults.appendChild(userDiv);
		});
	}, 300);
});

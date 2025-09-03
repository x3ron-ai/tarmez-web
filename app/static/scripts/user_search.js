const user_search_results = document.getElementById("user_search_results");
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
			user_search_results.innerHTML = "";
			return;
		}

		const users = await search_users(current_input);
		user_search_results.innerHTML = "";

		users.forEach(user => {
            const li = document.createElement("li");
            li.style.listStyle = "none";
            
            const a = document.createElement("a");
            a.textContent = user.username;
            a.href = `/chat/${user.id}`;
            a.style.textDecoration = "none";
            a.style.color = "inherit";
            
            li.appendChild(a);
            user_search_results.appendChild(li);
        });
	}, 300);
});

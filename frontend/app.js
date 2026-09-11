document.addEventListener('DOMContentLoaded', () => {
    const postForm = document.getElementById('postForm');
    const usernameInput = document.getElementById('username');
    const contentInput = document.getElementById('content');
    const postsList = document.getElementById('postsList');

    const pingForm = document.getElementById('pingForm');
    const pingTarget = document.getElementById('pingTarget');
    const pingOutput = document.getElementById('pingOutput');

// Fetching entries from the API (Hardened: textContent instead of innerHTML)
    async function fetchPosts() {
        try {
            const response = await fetch('/api/posts');
            const posts = await response.json();

            postsList.innerHTML = '';

            if (posts.length === 0) {
                postsList.innerHTML = '<p class="empty-msg">Brak wpisów w systemie.</p>';
                return;
            }

            posts.forEach(post => {
                const postCard = document.createElement('div');
                postCard.className = 'post-item';

                const authorDiv = document.createElement('div');
                authorDiv.className = 'post-author';
                authorDiv.textContent = post.author;

                const contentDiv = document.createElement('div');
                contentDiv.className = 'post-text';
                contentDiv.textContent = post.content;

                postCard.appendChild(authorDiv);
                postCard.appendChild(contentDiv);
                postsList.appendChild(postCard);
            });
        } catch (err) {
            console.error('Błąd pobierania wpisów:', err);
        }
    }

// Adding an entry
    postForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const author = usernameInput.value.trim();
        const content = contentInput.value.trim();

        if (!author || !content) return;

        try {
            const res = await fetch('/api/posts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ author, content })
            });

            if (res.ok) {
                postForm.reset();
                fetchPosts();
            }
        } catch (err) {
            console.error('Błąd zapisu wpisu:', err);
        }
    });

    // Ping tool
    pingForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        pingOutput.style.display = 'block';
        pingOutput.textContent = 'Sprawdzanie połączenia...';

        try {
            const res = await fetch('/api/ping', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target: pingTarget.value.trim() })
            });
            const data = await res.json();
            pingOutput.textContent = data.output;
        } catch (err) {
            pingOutput.textContent = 'Wystąpił błąd komunikacji z serwerem.';
        }
    });

    fetchPosts();
});

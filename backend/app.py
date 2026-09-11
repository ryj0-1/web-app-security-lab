import sqlite3
import subprocess
import re
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='/var/www/html', static_url_path='')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# API: Downloading entries
@app.route('/api/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    posts_raw = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(post) for post in posts_raw])

# API: Adding a new entry
@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data or 'author' not in data or 'content' not in data:
        return jsonify({"error": "Brakujące dane"}), 400

    author = data['author']
    content = data['content']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO posts (author, content) VALUES (?, ?)',
        (author, content)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Wpis zapisany!"}), 201

# API: Searching for entries (Hardering against SQLi INJECTION)
@app.route('/api/search', methods=['GET'])
def search_posts():
    query = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor()

    # CORRECT: The ? sign as a placeholder.
    # The search value is passed separately as a tuple, rather than being concatenated into the SQL string.
    search_param = f"%{query}%"
    sql = "SELECT * FROM posts WHERE content LIKE ?"
    results_raw = cursor.execute(sql, (search_param,)).fetchall()
    conn.close()

    return jsonify([dict(row) for row in results_raw])

# API: PING diagnostic tool (Hardering against Command Injection)
@app.route('/api/ping', methods=['POST'])
def ping_host():
    data = request.get_json()
    host = data.get('target', '').strip()

    if not host:
        return jsonify({"error": "Brak celu do sprawdzenia"}), 400

	# Whitelist input validation
    # Allow only letters, numbers, dots, and hyphens (standard domain/IP).
    # Reject separators: ;, &, |, `, $, spaces, etc.
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        return jsonify({"output": "Błąd: Niedozwolone znaki w adresie docelowym!"}), 400

    # Executed directly without shell (shell=False)
    cmd = ["ping", "-c", "1", host]

    try:
        output = subprocess.check_output(cmd, shell=False, stderr=subprocess.STDOUT, text=True)
        return jsonify({"output": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"output": e.output}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

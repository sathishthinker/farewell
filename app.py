from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=BASE_DIR)
CORS(app)

DB_PATH = os.path.join(BASE_DIR, 'farewell.db')

# ─── DATABASE SETUP ──────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT    NOT NULL,
                type      TEXT    NOT NULL CHECK(type IN ('roast', 'toast')),
                message   TEXT    NOT NULL,
                created_at TEXT   NOT NULL
            )
        ''')
      
        

# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/entries', methods=['GET'])
def get_entries():
    """Return all roast/toast entries, newest first."""
    with get_db() as conn:
        rows = conn.execute(
            'SELECT id, name, type, message, created_at FROM entries ORDER BY id DESC'
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route('/api/entries', methods=['POST'])
def add_entry():
    """Add a new roast or toast entry."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    name    = (data.get('name')    or '').strip()
    typ     = (data.get('type')    or '').strip().lower()
    message = (data.get('message') or '').strip()

    # Validation
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    if typ not in ('roast', 'toast'):
        return jsonify({'error': 'type must be roast or toast'}), 400
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    if len(name) > 100:
        return jsonify({'error': 'Name too long (max 100 chars)'}), 400
    if len(message) > 1000:
        return jsonify({'error': 'Message too long (max 1000 chars)'}), 400

    created_at = datetime.utcnow().isoformat()
    with get_db() as conn:
        cursor = conn.execute(
            'INSERT INTO entries (name, type, message, created_at) VALUES (?, ?, ?, ?)',
            (name, typ, message, created_at)
        )
        conn.commit()
        new_id = cursor.lastrowid

    return jsonify({
        'id': new_id,
        'name': name,
        'type': typ,
        'message': message,
        'created_at': created_at
    }), 201


# ─── MAIN ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    print("✅  Database ready:", DB_PATH)
    print("🚀  Starting server at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

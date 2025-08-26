from flask import Flask, render_template, request, redirect, session, jsonify, send_from_directory, url_for
import sqlite3, os, time
from werkzeug.utils import secure_filename
from functools import wraps


app = Flask(__name__)
app.secret_key = "yepthisisverysecretkey"
DB = os.path.join(os.path.dirname(__file__), "database.db")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
AVATAR_DIR = os.path.join(UPLOAD_DIR, "avatars")
FILE_DIR = os.path.join(UPLOAD_DIR, "files")
VOICE_DIR = os.path.join(UPLOAD_DIR, "voice")
for d in [UPLOAD_DIR, AVATAR_DIR, FILE_DIR, VOICE_DIR]:
    os.makedirs(d, exist_ok=True)

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            avatar TEXT
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            content TEXT,
            file_path TEXT,
            voice_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.commit()

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    if "username" in session:
        return redirect("/chat")
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()
        with get_db() as conn:
            row = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        if row:
            session["username"] = username
            return redirect("/chat")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()
        avatar = request.files.get("avatar")
        avatar_path = None
        if avatar and avatar.filename:
            fname = secure_filename(f"{username}_{int(time.time())}_{avatar.filename}")
            avatar.save(os.path.join(AVATAR_DIR, fname))
            avatar_path = f"avatars/{fname}"
        try:
            with get_db() as conn:
                conn.execute("INSERT INTO users (username, password, avatar) VALUES (?,?,?)", (username, password, avatar_path))
                conn.commit()
            session["username"] = username
            return redirect("/chat")
        except sqlite3.IntegrityError:
            return render_template("signup.html", error="Username already exists")
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/chat")
@login_required
def chat():
    if "username" not in session:
        return redirect("/login")
    username = session["username"]
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    avatar_url = url_for("uploaded_file", filename=user["avatar"]) if user and user["avatar"] else url_for("static", filename="default-avatar.png")
    return render_template("chat.html", username=username, avatar_url=avatar_url)

@app.route("/api/messages", methods=["GET", "POST"])
def api_messages():
    if "username" not in session:
        return jsonify({"error":"unauthorized"}), 401
    if request.method == "POST":
        sender = session["username"]
        content = request.form.get("content","").strip()
        file = request.files.get("file")
        voice = request.files.get("voice")
        file_path = None
        voice_path = None
        if file and file.filename:
            fname = secure_filename(f"{sender}_{int(time.time())}_{file.filename}")
            file.save(os.path.join(FILE_DIR, fname))
            file_path = f"files/{fname}"
        if voice and voice.filename:
            vname = secure_filename(f"{sender}_{int(time.time())}_{voice.filename}")
            voice.save(os.path.join(VOICE_DIR, vname))
            voice_path = f"voice/{vname}"
        with get_db() as conn:
            conn.execute("INSERT INTO messages (sender, content, file_path, voice_path) VALUES (?,?,?,?)", (sender, content, file_path, voice_path))
            conn.commit()
        return jsonify({"status":"ok"})
    else:
        with get_db() as conn:
            msgs = conn.execute("SELECT * FROM messages ORDER BY id ASC LIMIT 200").fetchall()
        out = []
        for m in msgs:
            out.append(dict(m))
        return jsonify(out)

@app.route("/profile", methods=["POST"])
@login_required
def profile():
    if "username" not in session:
        return redirect("/login")
    avatar = request.files.get("avatar")
    if avatar and avatar.filename:
        username = session["username"]
        fname = secure_filename(f"{username}_{int(time.time())}_{avatar.filename}")
        avatar.save(os.path.join(AVATAR_DIR, fname))
        with get_db() as conn:
            conn.execute("UPDATE users SET avatar=? WHERE username=?", (f"avatars/{fname}", username))
            conn.commit()
    return redirect("/chat")

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "uploads"), filename)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
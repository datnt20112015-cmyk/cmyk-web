import hashlib
import os
import sqlite3

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

DB_PATH = os.path.join(os.path.dirname(__file__), "app_data.db")
ADMIN_ACCESS_CODE = "ADMIN2026"

app = Flask(__name__)
app.secret_key = "smart-app-secret-key-2026"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            full_name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", ("admin",))
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
            ("admin", hash_password("admin123"), "Quản trị viên"),
        )
    conn.commit()
    conn.close()


def is_logged_in():
    return "user" in session


def current_user():
    return session.get("user")


def app_settings():
    return session.get("settings", {"theme": "light", "reduce_motion": False})


@app.route("/")
def index():
    if is_logged_in():
        if current_user().get("role") == "admin":
            return redirect(url_for("admin"))
        return redirect(url_for("dashboard"))
    return render_template("guest.html", settings=app_settings())


@app.route("/guest")
def guest():
    return render_template("guest.html", settings=app_settings())


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        theme = request.form.get("theme", "light")
        if theme not in {"light", "dark"}:
            theme = "light"
        session["settings"] = {
            "theme": theme,
            "reduce_motion": request.form.get("reduce_motion") == "on",
        }
        flash("Đã lưu cài đặt.", "success")
        return redirect(url_for("settings"))

    return render_template("settings.html", settings=app_settings(), user=current_user())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        admin_code = request.form.get("admin_code", "").strip()

        if admin_code and admin_code == ADMIN_ACCESS_CODE:
            session["user"] = {"username": "admin", "full_name": "Quản trị viên", "role": "admin"}
            flash("Đăng nhập admin thành công!", "success")
            return redirect(url_for("admin"))

        if not username or not password:
            flash("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.", "error")
            return render_template("login.html")

        conn = get_db()
        user = conn.execute(
            "SELECT username, full_name FROM users WHERE username = ? AND password = ?",
            (username, hash_password(password)),
        ).fetchone()
        conn.close()

        if user is None:
            flash("Tài khoản hoặc mật khẩu không đúng.", "error")
            return render_template("login.html")

        session["user"] = {
            "username": user["username"],
            "full_name": user["full_name"],
            "role": "user",
        }
        flash(f"Chào mừng {user['full_name']}!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm_password", "").strip()

        if not full_name or not username or not password or not confirm:
            flash("Vui lòng điền đầy đủ thông tin.", "error")
            return render_template("register.html")

        if password != confirm:
            flash("Mật khẩu xác nhận không khớp.", "error")
            return render_template("register.html")

        if len(password) < 4:
            flash("Mật khẩu phải có ít nhất 4 ký tự.", "error")
            return render_template("register.html")

        conn = get_db()
        exists = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
        if exists:
            conn.close()
            flash("Tên đăng nhập đã tồn tại.", "error")
            return render_template("register.html")

        conn.execute(
            "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
            (username, hash_password(password), full_name),
        )
        conn.commit()
        conn.close()

        flash("Đăng ký thành công! Bạn có thể đăng nhập ngay.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=current_user(), settings=app_settings())


@app.route("/chat")
def chat():
    conn = get_db()
    rows = conn.execute(
        "SELECT id, username, full_name, message, created_at "
        "FROM chat_messages ORDER BY id DESC LIMIT 100"
    ).fetchall()
    conn.close()
    messages = [dict(row) for row in reversed(rows)]
    return render_template(
        "chat.html", messages=messages, user=current_user(), settings=app_settings()
    )


@app.route("/api/chat/messages", methods=["GET", "POST"])
def chat_messages():
    if request.method == "GET":
        after_id = max(request.args.get("after", 0, type=int), 0)
        conn = get_db()
        rows = conn.execute(
            "SELECT id, username, full_name, message, created_at "
            "FROM chat_messages WHERE id > ? ORDER BY id LIMIT 100",
            (after_id,),
        ).fetchall()
        conn.close()
        return jsonify(messages=[dict(row) for row in rows])

    if not is_logged_in():
        return jsonify(error="Bạn cần đăng nhập để gửi tin nhắn."), 401

    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")
    if not isinstance(message, str):
        message = ""
    message = message.strip()
    if not message:
        return jsonify(error="Tin nhắn không được để trống."), 400
    if len(message) > 500:
        return jsonify(error="Tin nhắn tối đa 500 ký tự."), 400

    user = current_user()
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO chat_messages (username, full_name, message) VALUES (?, ?, ?)",
        (user["username"], user.get("full_name", user["username"]), message),
    )
    row = conn.execute(
        "SELECT id, username, full_name, message, created_at "
        "FROM chat_messages WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone()
    conn.commit()
    conn.close()
    return jsonify(message=dict(row)), 201


@app.route("/admin")
def admin():
    if not is_logged_in() or current_user().get("role") != "admin":
        flash("Bạn cần mã admin để truy cập trang quản trị.", "error")
        return redirect(url_for("login"))

    conn = get_db()
    users = conn.execute("SELECT id, username, full_name FROM users ORDER BY id").fetchall()
    conn.close()
    return render_template("admin.html", user=current_user(), users=users)


@app.route("/admin/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if not is_logged_in() or current_user().get("role") != "admin":
        return redirect(url_for("login"))

    conn = get_db()
    target = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
    if target and target["username"] == "admin":
        conn.close()
        flash("Không thể xóa tài khoản admin gốc.", "error")
        return redirect(url_for("admin"))

    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash("Đã xóa tài khoản thành công.", "success")
    return redirect(url_for("admin"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Bạn đã đăng xuất.", "success")
    return redirect(url_for("login"))


init_db()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

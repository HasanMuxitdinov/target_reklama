
from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "users.db"


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()

        if not first_name or not last_name:
            return "Ism va familiyangizni kiriting.", 400

        if len(first_name) > 60 or len(last_name) > 60:
            return "Ism yoki familiya juda uzun.", 400

        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                """
                INSERT INTO users (first_name, last_name, created_at)
                VALUES (?, ?, ?)
                """,
                (
                    first_name,
                    last_name,
                    datetime.now().isoformat(timespec="seconds")
                )
            )

        return render_template(
            "success.html",
            first_name=first_name
        )

    return render_template("register.html")


init_db()

if __name__ == "__main__":
    app.run(debug=True)

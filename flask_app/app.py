from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = "super_secret_key"

socketio = SocketIO(app)

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")

        if username and len(username) > 2:
            session["user"] = username
            return redirect(url_for("chat"))
        else:
            flash("Username must be at least 3 characters")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("chat.html", username=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@socketio.on("connect")
def handle_connect():
    if "user" not in session:
        return False 
    print(f"{session['user']} connected")


@socketio.on("message")
def handle_message(msg):
    username = session.get("user", "Unknown")

    print(f"{username}: {msg}")

    emit("message", {
        "user": username,
        "msg": msg
    }, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)

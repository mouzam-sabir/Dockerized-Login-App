from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "docker_login_secret_key"


# -----------------------------
# Database Connection
# -----------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="root123",
        database="docker_login"
    )


# -----------------------------
# Login
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(user["password"], password):

            session["username"] = username

            return redirect("/dashboard")

        flash("Invalid Username or Password", "danger")

        return redirect("/")

    return render_template("login.html")


# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            flash("Passwords do not match", "danger")

            return redirect("/register")

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()
            connection.close()

            flash("Username already exists", "warning")

            return redirect("/register")

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users(username,password)
            VALUES(%s,%s)
            """,
            (username, hashed_password)
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Registration Successful. Please Login.", "success")

        return redirect("/")

    return render_template("register.html")


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if "username" not in session:

        return redirect("/")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully", "success")

    return redirect("/")


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )



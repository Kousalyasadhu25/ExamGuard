from flask import Flask, request, render_template, session, redirect  
from database import init_db , get_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "examguard-security-key" 
init_db()

@app.route("/")
def home():
    return "Welcome to Exam Guard"


# @app.route("/register", methods=["GET", "POST"])
# def register():

#     if request.method == "POST":
#         name = request.form["name"]
#         email = request.form["email"]
#         password = request.form["password"]

#         print("name:", name)
#         print("email:", email)
#         print("password:", password)

#     return render_template("register.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        print(f"{name},Emai; : {email},Password :{hashed_password}")

        connection = get_db()
        connection.execute(
            """
            INSERT INTO candidates
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, password)
        )
        
        connection.commit()
        connection.close()
        
        #return "registration successful"
        return redirect("/login")

        print("name:", name)
        print("email:", email)
        print("password:", password)

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db()

        candidate = connection.execute(
            """
            SELECT *
            FROM candidates
            WHERE email = ? 
            """,
            (email,)
        ).fetchone()

        connection.close()

        if candidate and check_password_hash(candidate["password"],password):
           # return "Login successful!"
           session["candidate_id"]= candidate["id"]
           #return "Login successful!"
           #return render_template("dashboard.html")
           return redirect("/dashboard")
        
        return "Invalid email or password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "candidate id" not in session:
        return "please login first"


    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return "logout successful"


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
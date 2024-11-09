# demo of flask-login

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "app_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

users = {"testuser":{"password": "testpass"}}

# user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id
    
    @staticmethod
    def get(user_id):
        return User(user_id) if user_id in users else None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("home.html", user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            flash("Login Successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

# dashboard route (protected)
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

# logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
# demo of flask-login

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import uuid

app = Flask(__name__)
app.secret_key = "app_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

users = {} # {uuid4:user object}

# user model with password hashing
class User(UserMixin):
    def __init__(self, username, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get(user_id):
        return users.get(user_id)

    @staticmethod
    def get_by_username(username):
        for user in users.values():
            if user.username == username:
                return user
            return None

# Flask login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("home.html", user=current_user)

# register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if User.get_by_username(username):
            flash('Username already exists. Please choose another one.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username, password)
        users[new_user.id] = new_user
        # print(users)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.get_by_username(username)
        if user and user.verify_password(password):
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
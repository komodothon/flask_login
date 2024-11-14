# demo of flask-login

from flask import Flask, render_template, redirect, url_for, request, flash, g
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from os.path import join
import sqlite3
import uuid

DATABASE = join('instance', 'users.db')

app = Flask(__name__)
app.secret_key = "app_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

# database helper functions
def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

def add_user(prepped_user_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (id, username, email, password_hash) VALUES (?, ?, ?, ?)", prepped_user_data)
    connection.commit()

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# user model with password hashing
class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        return User(*user_data) if user_data else None # * used for unpacking into a tuple, whatever is inside
        
    @staticmethod
    def get_by_username(username):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        return User(*user_data) if user_data else None

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    

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
        email = request.form.get('email')
        password = request.form.get('password')

        if User.get_by_username(username):
            flash('Username already exists. Please choose another one.', 'danger')
            return redirect(url_for('register'))

        id = str(uuid.uuid4())
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(id, username, email, password_hash)
        prepped_user_data = (id, username, email, password_hash)
        add_user(prepped_user_data)

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
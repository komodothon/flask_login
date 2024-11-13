# User Authentication System using flask_login
flask_login library exercises

### Features

- **User Model with Hashed Passwords**  
  - Securing user data by storing hashed passwords.
  - Using Bcrypt hash to secure the passwords and verification.

- **Registration and Login Forms**  
  - Forms for new user registration and existing user login, with validation.

- **Flask-Login Integration**  

  - Essential methods and classes:
    - `LoginManager`: Managing and authenticating user sessions.
    - `login_user`: Logs in a user and creates a session.
    - `logout_user`: Logs out the current user and ends the session.
    - `current_user`: Accesses the currently logged-in user.
    - `login_required`: Restricts view access to authenticated users only.

- **Session Protection for Enhanced Security**  
  - Ensures sessions are protected to prevent unauthorized access and increase security.


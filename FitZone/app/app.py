from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
# from setup_db import User, Gym, ToDo

import os
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))
app.secret_key = "abc123"  # 🔐 use environment var in production

# Database setup
engine = create_engine("sqlite:///FITZONE.db")
Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/')
def index():
    return render_template('index.html')  # ⬅️ This WILL work if file exists

@app.route('/sign_up_test', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not password or not confirm_password:
            flash("All fields are required.", "danger")
            return render_template("sign_up_test.html")

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return render_template('sign_up_test.html')

        # existing_user = db_session.query(User).filter_by(username=username).first()
        # if existing_user:
        #     flash("Username already exists", "danger")
        #     return render_template('sign_up_test.html')

        # hashed_password = generate_password_hash(password)
        # new_user = User(username=username, password=hashed_password)
        # db_session.add(new_user)
        # db_session.commit()

        flash("You have successfully signed up", "success")
        return redirect(url_for('login'))

    return render_template('sign_up_test.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # user = db_session.query(User).filter_by(username=username).first()
        # if user and check_password_hash(user.password, password):
        #     session["user"] = username
        #     flash("You have successfully logged in", "success")
        #     return redirect(url_for('dashboard'))

        flash("Invalid username or password", "danger")
        return render_template('login.html')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
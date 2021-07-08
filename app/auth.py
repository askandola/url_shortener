from flask import Blueprint, request, render_template, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

@auth.route("/signup", methods=['GET', 'POST'])
def signup() :
    if request.method=="POST" :
        email = request.form.get('email')
        password = request.form.get('password')
        if len(password)<8 or len(password)>30 :
            flash("Your password length must be between 8 and 30 characters.", "danger")
            return redirect("/signup")
        user_check = User.query.filter_by(email=email).first()
        if user_check is not None :
            flash("Email already registered", "warning")
            return redirect("/signup")
        entry = User(email=email, password_hash=generate_password_hash(password))
        db.session.add(entry)
        db.session.commit()
        session['user'] = entry.id
        return redirect("/")
    return render_template("auth/signup.html")

@auth.route("/login", methods=['GET', 'POST'])
def login() :
    if request.method=='POST' :
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user is None or not check_password_hash(user.password_hash, password) :
            flash("Invalid email or password", "danger")
            return redirect("/login")
        session['user'] = user.id
        return redirect("/")
    return render_template("auth/login.html")

@auth.route("/logout", methods=['GET'])
def signout() :
    if 'user' in session :
        session.pop('user')
        return redirect("/")
    flash("Please login to continue.", "warning")
    return redirect("/login")

@auth.route("/change-email", methods=['GET', 'POST'])
def change_email() :
    if 'user' in session :
        user = User.query.filter_by(id=session['user']).first()
        if request.method=="POST" :
            password = request.form.get('password')
            new_email = request.form.get('email')
            if not check_password_hash(user.password_hash, password) :
                flash("Wrong password", "danger")
                return redirect("/change-email")
            check_email = User.query.filter_by(email=new_email).first()
            if check_email is not None :
                flash("Email already registered", "danger")
                return redirect("/change-email")
            user.email = new_email
            db.session.commit()
            flash("Email changed successfully", "success")
            return redirect("/")
        return render_template("auth/change_email.html")
    flash("Please login to continue.", "warning")
    return redirect("/login")

@auth.route("/change-password", methods=['GET', 'POST'])
def change_password() :
    if 'user' in session :
        user = User.query.filter_by(id=session['user']).first()
        if request.method=="POST" :
            password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            if not check_password_hash(user.password_hash, password) :
                flash("Wrong password", "danger")
                return redirect("/change-password")
            if len(new_password)<8 or len(new_password)>30 :
                flash("Your new password length must be betweeen 8 and 30 characters", "danger")
                return redirect("/change-password")
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            flash("Password changed successfully", "success")
            return redirect("/")
        return render_template("auth/change_password.html")
    flash("Please login to continue.", "warning")
    return redirect("/login")

@auth.route("/delete-account", methods=['GET', 'POST'])
def delete_account() :
    if 'user' in session :
        user = User.query.filter_by(id=session['user']).first()
        if request.method=='POST' :
            password = request.form.get('password')
            if not check_password_hash(user.password_hash, password) :
                flash("Wrong password", "danger")
                return redirect("/delete-account")
            session.pop('user')
            db.session.delete(user)
            db.session.commit()
            flash("Account deleted successfully", "success")
            return redirect("/")
        return render_template("auth/delete_account.html")
    flash("Please login to continue.", "warning")
    return redirect("/login")
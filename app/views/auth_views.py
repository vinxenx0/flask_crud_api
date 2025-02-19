from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from app.models.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

auth_views = Blueprint("auth_views", __name__)

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField("Contraseña", validators=[InputRequired(), Length(min=6, max=50)])
    submit = SubmitField("Login")

@auth_views.route("/")
def home():
    return render_template("index.html")

@auth_views.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            token = create_access_token(identity=user.id)
            return render_template("dashboard.html",token=token)
            #return jsonify({"message": "Login exitoso", "token": token}), 200  # ✅ Devuelve JSON con token
        
        else:
            return jsonify({"message": "Usuario o contraseña incorrectos"}), 401  # ✅ Devuelve error JSON
    
    return render_template("login.html", form=form)

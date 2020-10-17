from flask import Flask,render_template,redirect,url_for,get_flashed_messages,flash
import flask
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    EqualTo
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "alsdkjflkqjletkjalsdf"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Log in")

class RegisterForm(FlaskForm):
    username = StringField("Username",[DataRequired()])
    password = PasswordField("Password",[DataRequired()])
    confirm = PasswordField("Repeat Password",[DataRequired()])
    submit = SubmitField("Register")

@app.route("/",methods = ["GET","POST"])
def index():

    form = LoginForm()

    if form.validate_on_submit():
        pass

    return render_template("index.html",form=form)

@app.route("/register",methods=["GET","POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm = form.confirm.data

        if(password == confirm):
            newUser = UserModel(username,password)
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            flash("Passwords must match","error")
        
    return render_template("register.html",form=form)

if __name__ == "__main__":
    from database import UserModel,db
    db.init_app(app)
    app.run(debug=True,port=80)
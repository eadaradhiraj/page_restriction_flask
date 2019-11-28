from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.secret_key = 'any random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    subscription = db.Column(db.String(1))


class page_details(db.Model):
    subscription_class = db.Column(db.String(1), primary_key=True)
    start_page = db.Column(db.Integer)
    end_page = db.Column(db.Integer)


@app.route("/")
def index():
    return render_template("index.html", sess=session)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]

        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            session['username'] = uname
            session['subscription'] = login.subscription
            return redirect(url_for("index"))
        else:
            return render_template("login.html", wrong_cred=True)
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        subscription = request.form['subscription']
        passw = request.form['passw']

        register = user(username=uname, password=passw,
                        subscription=subscription)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/page_admin")
def page_admin():
    if session['username'] == 'admin':
        return render_template("table.html", page_details=page_details.query.all())
    else:
        return redirect(url_for('subscription'))


@app.route("/update_page_details", methods=["POST"])
def update_page_details():
    page_details.query.delete()
    for row in json.loads(request.data):
        db.session.add(
            page_details(
                subscription_class=row['subscription_class'],
                start_page=row['start_page'],
                end_page=row['end_page']
            )
        )
    db.session.commit()
    return "OK"

@app.route("/subscription")
def subscription():
    return render_template("subscription.html")

@app.route('/a<string:text>')
def all_routes(text):
    current_pg_dets = page_details.query.filter_by(
        subscription_class=session['subscription']).first()
    if (session['subscription'] == current_pg_dets.subscription_class) and (current_pg_dets.start_page <= int(text) <= current_pg_dets.end_page):
        return render_template("index.html", sess=session)
    else:
        return redirect(url_for('subscription'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

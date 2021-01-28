from flask import render_template, redirect, abort, url_for, request
from werkzeug.utils import html
from forum import app, db, bcrypt
from forum.forms import registration_form, login_form, topic_form
from forum.models import User, Topic
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    topics = Topic.query.all()
    return render_template("home.html", topics = topics)

@app.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")

    form = registration_form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect("/")

    return render_template("register.html", form = form)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    form = login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect("/")

    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/topic/new", methods = ["GET", "POST"])
@login_required
def new_topic():
    form = topic_form()
    if form.validate_on_submit():
        topic = Topic(header = form.header.data, content = form.content.data, author = current_user)
        db.session.add(topic)
        db.session.commit()
        return redirect("/")

    return render_template("create_topic.html", form = form)

@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    return render_template("topic.html", topic = topic)
    
@app.route("/topic/<int:topic_id>/update", methods = ["GET", "POST"])
@login_required
def update_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    if topic.author != current_user:
        abort(403)

    form = topic_form()
    if form.validate_on_submit():
        topic.header = form.header.data
        topic.content = form.content.data
        db.session.commit()
        return redirect(url_for("topic", topic_id = topic.id))
    elif request.method == "GET":
        form.header.data = topic.header
        form.content.data = topic.content

    return render_template("create_topic.html", form = form)

@app.route("/topic/<int:topic_id>/delete", methods = ["GET", "POST"])
@login_required
def delete_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    if topic.author != current_user:
        abort(403)

    db.session.delete(topic)
    db.session.commit()
    return redirect("/")
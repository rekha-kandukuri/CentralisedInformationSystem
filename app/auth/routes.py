from app import app, db, login
from app.forum.models import post
from app.utils import send_async_email, send_reset_email
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from flask import request, redirect, url_for, render_template, get_flashed_messages, flash, jsonify
from .forms import LoginForm, RegisterForm, RequestResetForm, ResetPasswordForm
from .models import User
from werkzeug.urls import url_parse
from flask_mail import Message
from threading import Thread
from app.auth import auth


@auth.route('/logout')
def logout():
    current_user.last_seen = datetime.utcnow()
    db.session.commit()
    logout_user()
    return redirect(url_for('home.index'))


@auth.route('/login', methods=['GET', 'POST'])
def loginUser():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Email or Password', category="danger")
            return redirect(url_for('auth.loginUser'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.index')
        return redirect(next_page)
    return render_template('signinpage.html', title='SignIn', form=form)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, user_role=form.user_role.data, Region=form.Region.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully Registered', category="success")
        msg = Message('Welcome to CELIS', sender="celis.students@gmail.com", recipients=[user.email])
        msg.body = "Hey There, We are happy that you have decided to join our community, We look forward to working with you. If you have any issues do notify us in our contact us section"
        Thread(target=send_async_email, args=(app, msg)).start()
        return redirect(url_for('auth.loginUser'))
    return render_template('signuppage.html', form=form, title='Register')


@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.loginUser'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = (form.password.data)
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.loginUser'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@auth.route('/profile/<username>')
@login_required
def profile(username):
    print(username)
    user = User.query.filter_by(username=username).first()
    if user:
        if user.user_role == "Instructor":
            posts = post.query.filter_by(user_id=user.id).all()
            no_posts = len(posts)
            c = user.provides_course.all()
            return render_template('profile_instructor.html', title='Profile', user=user, no_posts=no_posts, posts=posts, courses=c)
        elif user.user_role == "Student":
            posts = post.query.filter_by(user_id=user.id).all()
            no_posts = len(posts)
            courses = user.Courses_enrolled
            return render_template('profile_student.html', title='Profile', user=user, no_posts=no_posts, posts=posts, courses=courses)
    return redirect(url_for('auth.profile', username=current_user.username))

@auth.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    if current_user.is_authenticated:
        if request.method == 'POST':
            twitter_link = request.form['twitter_link']
            facebook_link = request.form['linkedin_link']
            instagram_link = request.form['github_link']
            birthdate = request.form['birthdate']
            about = request.form['interests']
            user = User.query.filter_by(id=current_user.id).first()
            user.twitter = twitter_link
            user.facebook = facebook_link
            user.instagram = instagram_link
            user.birthdate = birthdate
            user.Interests = about
            db.session.commit()
            flash('Changes Saved Successfully', category='success')
            return redirect(url_for('auth.profile', username=user.username))
        return render_template('edit_profile.html',)
    else:
        return redirect(url_for('index'))

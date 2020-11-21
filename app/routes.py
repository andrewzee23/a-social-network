import os
import secrets
from PIL import Image
from flask import url_for, render_template, flash, redirect, request, abort
from app import app, db, bcrypt, mail
# importing CLASSES from FORMS.py
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
# importing TABLES FROM DATABASE
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message



@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('home.html',posts=posts)


@app.route('/about')
def about():

    return render_template('about.html', title = 'About')










@app.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():

    form = PostForm()

    if form.validate_on_submit():
        # added post to the database
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', title = 'New Post', form = form, legend = 'New Post')


@app.route('/post/<int:post_id>', methods = ['GET', 'POST'])
def post(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post=post)


@app.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:

        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect( url_for('post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title = 'Update Post', form = form, legend = 'Update Post')


@app.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:

        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_posts(username):

    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page=page)
    return render_template('user_posts.html',posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = ''' 
To reset your password, visit the following link: {url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.'''

    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title= 'Reset Password', form = form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # added user to the database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html', title='Reset Password', form=form)


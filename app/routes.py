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






















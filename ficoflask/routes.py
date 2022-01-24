from flask import render_template, url_for, redirect, flash, request, session
from ficoflask import app, db, bcrypt
from ficoflask.forms import RegistrationForm, LoginForm, AccountUpdateForm, UploadImageForm
from ficoflask.models import User, UserDetails, Database
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from detect_fish import detect
import os
import numpy as np
from PIL import Image as im


@app.route('/', methods = ['POST','GET'])
@app.route('/homepage', methods = ['POST','GET'])
def homepage():
    form = UploadImageForm()
    if form.validate_on_submit():
        if current_user.id:
            if form.upload_image.data:
                image_file= homepageSaveImage(form.upload_image.data)
                image_url=app.root_path + '/static/image_data/' + image_file
                weight = 'D:/XAMPP/htdocs/Fico1/weights/best.pt'
                os.system('python detect_fish.py --weights ' + weight + ' --source ' + image_url +' --save-txt')
                image_url = url_for('static', filename="image_data/" + image_file)
                detected_image_url = url_for('static', filename="user_image_details/" + image_file)
                detected_image_txt = app.root_path + '/static/user_image_details/' + image_file
                txtname, txt_extension = os.path.splitext(detected_image_txt)
                with open( txtname + '.txt') as f:
                    fish_count = f.readline().rstrip()

                image_details = Database(image_file = image_url, detected_image = detected_image_url,
                                fish_count = fish_count, user_id = current_user.id)
                db.session.add(image_details)
                db.session.commit()

            return redirect(url_for('resultPage', image_url = image_url))
        else:
            flash('Please Login')
            return redirect(url_for('login'))

    return render_template('homepage.html', title = "Home", legend = "Welcome",
                            form = form)


def homepageSaveImage(picture_file):
    picture_name = secure_filename(picture_file.filename)
    picture_path = os.path.join(app.root_path, 'static/image_data', picture_name)
    picture_file.save(picture_path)
    return picture_name

@app.route('/takePhoto')
def takePhoto():
    form = UploadImageForm()
    if form.validate_on_submit():
        if current_user.id:
            if form.upload_image.data:
                image_file= homepageSaveImage(form.upload_image.data)
                image_url=app.root_path + '/static/image_data/' + image_file
                weight = 'D:/XAMPP/htdocs/Fico1/weights/best.pt'
                os.system('python detect_fish.py --weights ' + weight + ' --source ' + image_url +' --save-txt')
                image_url = url_for('static', filename="image_data/" + image_file)
                detected_image_url = url_for('static', filename="user_image_details/" + image_file)
                detected_image_txt = app.root_path + '/static/user_image_details/' + image_file
                txtname, txt_extension = os.path.splitext(detected_image_txt)
                with open( txtname + '.txt') as f:
                    fish_count = f.readline().rstrip()

                image_details = Database(image_file = image_url, detected_image = detected_image_url,
                                fish_count = fish_count, user_id = current_user.id)
                db.session.add(image_details)
                db.session.commit()

            return redirect(url_for('resultPage', image_url = image_url))
    return render_template('takePhoto.html', title = "Take Photo", form = form)

@app.route('/resultPage',  methods = ['POST','GET'])
def resultPage():
    image_url = request.args['image_url']
    data =  Database.query.where(Database.image_file == image_url).with_entities(Database.image_file, Database.detected_image, Database.fish_count)
    return render_template('resultPage.html', title = "Result", legend = "Your Result", resultData = data)

def profile_save_image(picture_file):
    picture_name = picture_file.filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_name)
    picture_file.save(picture_path)
    return picture_name

@app.route('/myProfile', methods = ['POST', 'GET'])
@login_required
def myProfile():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_file = profile_save_image(form.picture.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        user_details = UserDetails(firstname = form.firstname.data, lastname = form.lastname.data, user_id= current_user.id)
        db.session.add(user_details)
        db.session.commit()
        return redirect(url_for('myProfile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        if current_user.details:
            form.firstname.data = current_user.details[-1].firstname
            form.lastname.data = current_user.details[-1].lastname
        else:
            form.firstname.data = ""
            form.lastname.data = ""
    image_url=url_for('static', filename="profile_pics/" + current_user.image_file)
    return render_template('myProfile.html', title = "Profile", legend = "Your Profile",
                            form = form, image_url = image_url)

@app.route('/myDatabase', methods = ['POST', 'GET'])
@login_required
def myDatabase():
    data =  Database.query.filter_by(user_id = current_user.id).with_entities(Database.image_file, Database.detected_image, Database.fish_count, Database.date_created)
    return render_template('myDatabase.html', legend = "Saved Results", myData = data)

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('myProfile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username = form.username.data, email=form.email.data, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {form.username.data}', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title = "Register", form = form)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('myProfile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Login successfully for {form.username.data}', category='success')
            return redirect(url_for('homepage'))
        else:
            flash(f'Login unsuccessfully for {form.username.data}', category='danger')

    return render_template('login.html', title = "Login", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

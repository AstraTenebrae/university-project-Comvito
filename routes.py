from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from sqlalchemy import select

from forms import LoginForm, RegistrationForm, AddNewOfferForm
from db_tables import User, Offer
from api_settings import app, db


@app.route('/')
def index():
    return redirect(url_for('homepage'))


@app.route('/home')
def homepage() -> tuple:
    offers = db.session.scalars(
        select(Offer).where(Offer.is_hidden == False).order_by(Offer.id.desc())
    ).unique().all()
    return render_template('homepage.html', offers=offers), 200


@app.route('/sketch/', methods=['GET'])
def sketch_route() -> tuple:
    return render_template('sketch.html'), 200


@app.route('/sketch2/', methods=['GET'])
def sketch2_route() -> tuple:
    return render_template('sketch_online_viewer_net.html'), 200


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('homepage'))
    
    return render_template('login.html', title='Вход', form=form), 200


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('homepage'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/offer-creation', methods=['GET', 'POST'])
def offer_creation():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = AddNewOfferForm()
    if form.validate_on_submit():
        offer = Offer(
            offer_name=form.offer_name.data, 
            offer_description=form.offer_description.data, 
            user_id_offeror=current_user.id,
            conditions=form.conditions.data,
            is_hidden=False,
        )                                                                           ### Добавить сюда поддержку категорий, когда они будут реализованы
        db.session.add(offer)
        db.session.commit()
        flash('Предложение успешно создано')
        return redirect(url_for('homepage'))                                        ### Потом можно заменить на личный кабинет или страницу предложения
    return render_template('new_offer.html', title='Новое предложение', form=form)
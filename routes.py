from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from sqlalchemy import select, or_
import math

from forms import LoginForm, RegistrationForm, AddNewOfferForm
from db_tables import User, Offer, Category
from api_settings import app, db


@app.route('/')
def index():
    return redirect(url_for('homepage'))


@app.route('/home')
def homepage() -> tuple:
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '')
    category_id = request.args.get('category', None, type=int)


    offers_query = select(Offer).where(Offer.is_hidden == False)
    if search_query:
        offers_query = offers_query.where(
            or_(
                Offer.offer_name.ilike(f'%{search_query}%'),
                Offer.offer_description.ilike(f'%{search_query}%')
            )
        )
    if category_id:
        offers_query = offers_query.join(Offer.categories).where(Category.id == category_id)
    offers_query = offers_query.order_by(Offer.id.desc()).offset((page - 1) * per_page).limit(per_page)
    

    count_query = select(db.func.count()).select_from(offers_query.subquery())
    total_count = db.session.scalar(count_query)
    if not total_count:
        total_count = 0
    if per_page > 0:
        total_pages = math.ceil(total_count / per_page)
    else:
        total_pages = 1
    if page > total_pages and total_pages > 0:
        page = total_pages
    elif page < 1:
        page = 1
    

    offers_result = db.session.execute(offers_query).unique()
    offers = offers_result.scalars().all()
    
    all_categories = db.session.scalars(
        select(Category).order_by(Category.category_name)
    ).unique().all()


    return render_template(
        'homepage.html', 
        offers=offers, 
        page=page, 
        per_page=per_page,
        total_pages=total_pages,
        search_query=search_query,
        selected_category=category_id,
        all_categories=all_categories,
    ), 200


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
    categories = db.session.scalars(select(Category).order_by(Category.category_name)).unique().all()
    form.categories.choices = [(c.id, c.category_name) for c in categories]

    if form.validate_on_submit():
        offer = Offer(
            offer_name=form.offer_name.data, 
            offer_description=form.offer_description.data, 
            user_id_offeror=current_user.id,
            conditions=form.conditions.data,
            is_hidden=False,
        )
        db.session.add(offer)

        db.session.flush()
        
        for category_id in form.categories.data:
            category = db.session.get(Category, category_id)
            if category:
                offer.categories.append(category)
        db.session.commit()
        flash('Предложение успешно создано')
        return redirect(url_for('homepage'))                                        ### Потом можно заменить на личный кабинет или страницу предложения
    return render_template('new_offer.html', title='Новое предложение', form=form)
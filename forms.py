from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy

from api_settings import db
from db_tables import User

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'size': 64, 'maxlength': 64})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'size': 64, 'maxlength': 64})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={'size': 64, 'maxlength': 64})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()], render_kw={'size': 64})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={'size': 64, 'maxlength': 64})
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={'size': 64, 'maxlength': 64})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Регистрация')

    def validate_username(self, username):                                          # методы с названием validate_<название поля> используются WTForms как кастомные валидаторы
        user = db.session.scalar(sqlalchemy.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sqlalchemy.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        

class AddNewOfferForm(FlaskForm):
    offer_name = StringField('Название предложения', validators=[DataRequired()], render_kw={'size': 64, 'maxlength': 64})
    offer_description = TextAreaField('Описание предложения', validators=[DataRequired()], render_kw={
        'class': 'offer-creation-wide-textarea',
        'placeholder': 'Введите описание предложения здесь...',
        'rows': 10, 
        'cols': 63,
        'maxlength': 1024,
    })
#    category = StringField('Введите категорию товара', render_kw={'size': 64, 'maxlength': 64})                                               ###   Пока что временно сделаем категории строкой, потом можно будет выбирать из огромного списка с поиском
    conditions = TextAreaField('', render_kw={
        'class': 'offer-creation-wide-textarea',
        'placeholder': 'Введите условия обмена здесь...',
        'rows': 10, 
        'cols': 63,
        'maxlength': 512,
    })
    submit = SubmitField('Создать предложение')

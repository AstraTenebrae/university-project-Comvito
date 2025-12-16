from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime

from api_settings import db, app, login

@login.user_loader
def load_user(id):
  return db.session.get(User, int(id))

class User_Feedback(db.Model):                                          # отзыв на человека (репутация)
    __tablename__ = "userfeedback"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    user_id_sender: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)         # связано с User.id 
    user_id_recipient: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)      # связано с User.id

    sender = relationship(
        "User",
        foreign_keys=[user_id_sender],
        backref="sent_feedbacks",
        lazy="joined",
    )
    recipient = relationship(
        "User",
        foreign_keys=[user_id_recipient],
        backref="received_feedbacks",
        lazy="joined",
    )


class Feedback_Rating(db.Model):                                        # оценка отзыва другими пользователями
    __tablename__ = "rating"
    id: Mapped[int] = mapped_column(primary_key=True)
    feedback_id: Mapped[int] = mapped_column(ForeignKey("userfeedback.id", ondelete="CASCADE"), nullable=False)            # связано с User_Feedback.id
    rating: Mapped[bool] = mapped_column(nullable=True)                 # 0 = палец вниз, 1 = палец вверх
    user_id_rater: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)          # связано с User.id

    __table_args__ = (
        UniqueConstraint('user_id_rater', 'feedback_id', name='uq_user_feedback_rating'),
    )

    feedback: Mapped["User_Feedback"] = relationship(
        "User_Feedback",
        foreign_keys=[feedback_id],
        backref="ratings",
        lazy='joined',
    )
    rater: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id_rater],
        backref="given_ratings",
        lazy='joined',
    )

class Offer(db.Model):                                                  # предложение
    __tablename__ = "offer"
    id: Mapped[int] = mapped_column(primary_key=True)
    offer_name: Mapped[str] = mapped_column(nullable=False)
    offer_description: Mapped[str] = mapped_column(nullable=False)
    user_id_offeror: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)                # связано с User.id
#    category: Mapped[str] = mapped_column(nullable=True)
    conditions: Mapped[str] = mapped_column(nullable=True)
    is_hidden: Mapped[bool] = mapped_column(nullable=False, default=False)
    offer_status: Mapped[str] = mapped_column(nullable=False, default="АКТИВНО", server_default="АКТИВНО")                                           # ДОЛЖНО ПРИНИМАТЬ ТОЛЬКО ЗНАЧНИЯ "АКТИВНО", "УСПЕХ" И "ОТМЕНА"
    
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id_offeror],
        backref="offers",
        lazy='joined',
    )

    categories: Mapped[List["Category"]] = relationship(
        "Category",
        secondary="offer_category",  # ссылка на промежуточную таблицу
        back_populates="offers",
        lazy='joined',
    )

class Category(db.Model):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(nullable=False)

    offers: Mapped[List["Offer"]] = relationship(
        "Offer",
        secondary="offer_category",  # ссылка на промежуточную таблицу
        back_populates="categories",
        lazy='joined',
    )

class Offer_Category(db.Model):
    __tablename__ = "offer_category"
    id: Mapped[int] = mapped_column(primary_key = True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
    offer_id: Mapped[int] = mapped_column(ForeignKey("offer.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('category_id', 'offer_id', name='unique_offer_category'),
    )

class User(UserMixin, db.Model):                                                   # пользователь
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)                      # не сам пароль, а хэш от него
    phone_number: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    registration_date: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    last_seen_online: Mapped[datetime.datetime] = mapped_column(nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
import datetime

db = SQLAlchemy()

class User_Feedback(db.Model):                                          # отзыв на человека (репутация)
    __tablename__ = "userfeedback"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    user_id_sender: Mapped[int] = mapped_column(nullable=False)         # связано с User.id 
    user_id_recipient: Mapped[int] = mapped_column(nullable=False)      # связано с User.id

    sender = relationship(
        "User",
        foreign_keys=[user_id_sender],
        backref="sent_feedbacks",
        lazy="joined",
    )
    recipient = relationship(
        "User",
        foreign_keys=[user_id_sender],
        backref="received_feedbacks",
        lazy="joined",
    )


class Feedback_Rating(db.Model):                                        # оценка отзыва другими пользователями
    __tablename__ = "rating"
    id: Mapped[int] = mapped_column(primary_key=True)
    feedback_id: Mapped[int] = mapped_column(nullable=False)            # связано с User_Feedback.id
    rating: Mapped[bool] = mapped_column(nullable=True)                 # 0 = палец вниз, 1 = палец вверх
    user_id_rater: Mapped[int] = mapped_column(nullable=False)          # связано с User.id

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
    user_id_offeror: Mapped[int] = mapped_column(nullable=False)                # связано с User.id
    category: Mapped[str] = mapped_column(nullable=True)
    conditions: Mapped[str] = mapped_column(nullable=True)
    is_hidden: Mapped[bool] = mapped_column(nullable=False, default=False)
    
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id_offeror],
        backref="offers",
        lazy='joined',
    )

class User(db.Model):                                                   # пользователь
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    registration_date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    last_seen_online: Mapped[datetime.datetime] = mapped_column(nullable=False)


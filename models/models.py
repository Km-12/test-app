from sqlalchemy import Column, Integer, String, Text
from models.database import Base


class QuestionsContent(Base):
    __tablename__ = "questionscontent"
    id = Column(Integer, primary_key=True)
    number = Column(String(128), unique=True)
    question = Column(Text)
    answer = Column(Text)

    def __init__(self, number=None, question=None, answer=None):
        self.number = number
        self.question = question
        self.answer = answer

    def __repr__(self):
        return "<Title %r>" % (self.number)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))

    def __init__(self, user_name=None, hashed_password=None):
        self.user_name = user_name
        self.hashed_password = hashed_password

    def __repr__(self):
        return "<Name %r>" % (self.user_name)


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    answer_one = Column(Text)
    answer_two = Column(Text)
    answer_three = Column(Text)
    answer_four = Column(Text)
    answer_five = Column(Text)

    def __init__(
        self,
        user_name=None,
        answer_one=None,
        answer_two=None,
        answer_three=None,
        answer_four=None,
        answer_five=None,
    ):
        self.user_name = user_name
        self.answer_one = answer_one
        self.answer_two = answer_two
        self.answer_three = answer_three
        self.answer_four = answer_four
        self.answer_five = answer_five

    def __repr__(self):
        return "<Name %r>" % (self.user_name)


class AnswerExplanation(Base):
    __tablename__ = "answer_explanation"
    id = Column(Integer, primary_key=True)
    number = Column(String(128), unique=True)
    answer = Column(Text)
    explanation = Column(Text)

    def __init__(self, number=None, answer=None, explanation=None):
        self.number = number
        self.answer = answer
        self.explanation = explanation

    def __repr__(self):
        return "<Title %r>" % (self.number)

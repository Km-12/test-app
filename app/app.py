from flask import Flask, render_template, request
from models.models import QuestionsContent, User, Answer
from models.database import db_session
from flask import session, redirect, url_for
from app import key
from app.check import AnswerCheck
from app.util import StringUtil
from hashlib import sha256

# Flaskオブジェクトの生成
app = Flask(__name__)

# 暗号化
app.secret_key = key.SECRET_KEY


# 「/top」へアクセスがあった場合に、「top.html」を返す
@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html", status=status)


# 「/signup」へアクセスがあった場合に、「signup.html」を返す
@app.route("/signup")
def signup():
    status = request.args.get("status")
    return render_template("signup.html", status=status)


# 「/passinquiry」へアクセスがあった場合に、「passinquiry.html」を返す
@app.route("/passinquiry")
def passinquiry():
    return render_template("passinquiry.html")


# 「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/")
@app.route("/index")
def index():
    if "user_name" in session:
        name = session["user_name"] + "さん"
        all_question = QuestionsContent.query.all()
        status = request.args.get("status")
        return render_template(
            "index.html", name=name, status=status, all_question=all_question
        )
    else:
        return redirect(url_for("top", status=""))


# ログイン
@app.route("/login", methods=["post"])
def login():
    user_name = request.form["user_name"]
    password = request.form["password"]

    if StringUtil.is_string_none_or_empty(user_name):
        return redirect(url_for("top", status="empty"))
    elif StringUtil.is_string_none_or_empty(password):
        return redirect(url_for("top", status="empty"))

    user = User.query.filter_by(user_name=user_name).first()
    if user:
        hashed_password = sha256(
            (user_name + password + key.SALT).encode("utf-8")
        ).hexdigest()
        if user.hashed_password == hashed_password:
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top", status="wrong_password"))
    else:
        return redirect(url_for("top", status="user_notfound"))


# 新規登録
@app.route("/registar", methods=["post"])
def registar():
    user_name = request.form["user_name"]
    password = request.form["password"]

    if StringUtil.is_string_none_or_empty(user_name):
        return redirect(url_for("signup", status="empty"))
    elif StringUtil.is_string_none_or_empty(password):
        return redirect(url_for("signup", status="empty"))

    user = User.query.filter_by(user_name=user_name).first()
    if user:
        return redirect(url_for("signup", status="exist_user"))
    else:

        hashed_password = sha256(
            (user_name + password + key.SALT).encode("utf-8")
        ).hexdigest()
        user = User(user_name, hashed_password)
        db_session.add(user)
        db_session.commit()
        session["user_name"] = user_name
        return redirect(url_for("index"))


# 回答登録
@app.route("/submitAnswers", methods=["post"])
def submitAnswers():
    user_name = request.form["name"].replace("さん", "")
    answer = Answer.query.filter_by(user_name=user_name).first()
    if answer:
        return redirect(url_for("index", status="already_answered"))
    else:
        answers_list = []

        # 回答の取得
        answer_one = request.form["answer_select1"]
        answer_two = request.form["answer_select2"]
        answer_three = request.form["answer_select3"]
        answer_four = request.form["answer_select4"]
        answer_five = request.form["answer_select5"]

        answers_list.append(answer_one)
        answers_list.append(answer_two)
        answers_list.append(answer_three)
        answers_list.append(answer_four)
        answers_list.append(answer_five)

        result_check, result_score = AnswerCheck.answerslist_check(answers_list)
        if result_check == AnswerCheck.FAILURE:
            return redirect(url_for("index", status="failure"))
        elif result_check == AnswerCheck.NOT_ANSWERED:
            return redirect(url_for("index", status="not_answered"))

        answer = Answer(
            user_name, answer_one, answer_two, answer_three, answer_four, answer_five
        )
        db_session.add(answer)
        db_session.commit()

        return render_template("passinquiry.html", score=result_score)


# ログアウト
@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top"))


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))


class Data(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # checked: Mapped[bool] = mapped_column(Boolean)
    text: Mapped[str] = mapped_column(String)


with app.app_context():
    db.create_all()
    users1 = db.session.execute(db.select(User)).scalars()
    users = [i.email for i in users1]
    list1 = db.session.execute(db.select(Data).where()).scalars()
    lists = [i for i in list1]


@app.route('/')
def home():
    return render_template("index.html", list=lists)


@app.route('/sign-in', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user.password == password:
            login_user(user=user)
            return render_template('index.html', list=lists)
        else:
            flash("Invalid password buddy!")
    return render_template("signin.html")


@app.route('/sign-up', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form.get("email") not in users:
            new_user = User()
            new_user.email = request.form.get('email')
            new_user.password = request.form.get('password')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return render_template('index.html', list=lists)
        else:
            flash('Email already exists, signin instead')
            return render_template('signin.html')
    return render_template("signup.html")


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html', list=lists)


@app.route("/delete/<int:num1>", methods=['POST', 'GET'])
def delete(num1):
    with app.app_context():
        text = db.session.execute(db.select(Data).where(Data.id == num1)).scalar()
        db.session.delete(text)
        db.session.commit()
        list2 = db.session.execute(db.select(Data)).scalars()
        lists1 = [i for i in list2]
    return render_template('index.html', list=lists1)


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        with app.app_context():
            new = Data()
            new.text = request.form.get('input')
            print(request.form.get('input'))
            db.session.add(new)
            db.session.commit()
    list2 = db.session.execute(db.select(Data)).scalars()
    lists2 = [i for i in list2]
    return render_template('index.html', list=lists2)


if __name__ == '__main__':
    app.run(debug=True)

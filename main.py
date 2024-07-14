from datetime import datetime, timedelta

from flask import Flask, abort, redirect, render_template
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from data import db_session
from data.job_form import JobForm
from data.jobs import Jobs
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_sess = None

@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    
    jobs = []
    if current_user.is_authenticated:
        jobs = db_sess.query(Jobs).filter((Jobs.team_leader == current_user.id) | (Jobs.author == current_user.id)).all()
    return render_template("index.html", jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    if not current_user.is_authenticated:
        return redirect("/login")
    if form.validate_on_submit():
        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.collaborators = form.collaborators.data
        job.work_size = form.work_size.data
        job.start_date = datetime.now()
        delta = timedelta(hours=job.work_size)
        job.end_date = job.start_date + delta
        job.author = current_user.id
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template('add_job.html', title='Добавление работы', form=form)


@app.route('/job/<job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    if not current_user.is_authenticated:
        return redirect("/login")
    
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        abort(404)
    if not (current_user.id == job.author or current_user.id == 1):
        return redirect("/")
    job_form = JobForm()
    if job_form.validate_on_submit():
        job.job = job_form.job.data
        job.team_leader = job_form.team_leader.data
        job.collaborators = job_form.collaborators.data
        job.work_size = job_form.work_size.data
        job.is_finished = job_form.is_finished.data
        job.author = current_user.id
        db_sess.commit()
        return redirect("/")
    job_form.job.data = job.job
    job_form.collaborators.data = job.collaborators
    job_form.team_leader.data = job.team_leader
    job_form.work_size.data = job.work_size

    return render_template('add_job.html', title='Редактирование работы', form=job_form)


@app.route('/job/delete/<job_id>', methods=['GET', 'POST'])
def delete_job(job_id):
    if not current_user.is_authenticated:
        return redirect("/login")

    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        abort(404)
    if not (current_user.id == job.author or current_user.id == 1):
        return redirect("/")
    db_sess.delete(job)
    db_sess.commit()
    return redirect("/")


def main():
    db_session.global_init("db/marsians.sqlite")
    global db_sess
    db_sess = db_session.create_session()
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()

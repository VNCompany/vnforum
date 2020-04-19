from .__imports import *
from forms.login_form import LoginForm
from sqlalchemy.orm import Session
from flask_login import login_user


class LoginController(Controller):
    __view__ = "login"
    __title__ = "Авторизация"

    form = None

    def __init__(self):
        super(LoginController, self).__init__()
        self.form = LoginForm()
        self.css("register.css")

    def view(self, session: Session, **kwargs):
        if self.form.validate_on_submit():
            status = DataBaseWorker.check_user(
                session=session,
                login=self.form.login.data,
                pw=self.form.password.data
            )
            if status[0] == "ok":
                login_user(status[1], remember=self.form.remember_me.data)
                return redirect("/index")
            else:
                return super(LoginController, self).view(form=self.form, error=status[0])
        else:
            return super(LoginController, self).view(form=self.form)

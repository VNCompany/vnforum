from .__imports import *
from forms.register_form import RegisterForm
from sqlalchemy.orm import Session

from models.user_model import User


class RegisterController(Controller):
    __view__ = "register"
    __title__ = "Регистрация"

    form = None

    def __init__(self):
        super(RegisterController, self).__init__()
        self.form = RegisterForm()
        self.css("register.css")

    def view(self, session: Session, **kwargs):
        if self.form.validate_on_submit():
            user = User(
                login=self.form.login.data,
                email=self.form.email.data,
                nickname=self.form.nickname.data,
                sex=self.form.sex.data,
            )
            user.set_password(self.form.password.data)
            status = DataBaseWorker.add_user(session, user)
            if status == "ok":
                return redirect("/index")
            else:
                return super(RegisterController, self).view(form=self.form, error=status)

        else:
            return super(RegisterController, self).view(form=self.form)

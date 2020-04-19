from .__imports import *
from models.user_model import User


class AdminController(Controller):
    __view__ = "admin"
    __title__ = "Админ-панель"

    def __init__(self):
        super(AdminController, self).__init__()
        self.users = self.db_session.query(User).all()
        self.css("admin.css")

    def view(self, **kwargs):
        return super(AdminController, self).view(users=self.users,
                                                 get_actions=self.get_actions)

    @staticmethod
    def get_actions(user: User):
        if user.status == 1:
            return f'''
            <a href="/user/{user.id}/set_perm?status=admin">Make admin</a>
            <a href="/user/{user.id}/set_perm?status=block">Block</a>
            '''
        elif user.status == 2:
            return f'''
            <a href="/user/{user.id}/set_perm?status=user">Make user</a>
            <a href="/user/{user.id}/set_perm?status=block">Block</a>
            '''
        elif user.status == 3:
            return f'''
            <a href="/user/{user.id}/set_perm?status=admin">Make admin</a>
            <a href="/user/{user.id}/set_perm?status=user">Unblock</a>
            '''
        else:
            return "None"

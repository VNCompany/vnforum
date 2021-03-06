from flask import redirect, url_for, render_template
from flask_login import current_user
from components.pagination import html_pagination
from db_session import create_session


class Controller:
    __view__ = None
    __title__ = "Page"
    view_includes = {}

    jquery_enabled = True
    db_session = None

    def __init__(self):
        self.view_includes.clear()
        self.view_includes["css"] = ""
        self.css("main.css")
        self.view_includes["js"] = ""
        self.javascript("jquery.js", "main.js")
        self.db_session = create_session()

    @staticmethod
    def static(path: str):
        return url_for('static', filename=path)

    def view(self, **kwargs):
        if self.__view__ is None:
            raise AttributeError
        elif current_user.is_authenticated and current_user.is_banned():
            return redirect("/logout")
        else:
            return render_template(str(self.__view__).replace(".", "/") + ".html",
                                   **kwargs,
                                   **self.view_includes,
                                   title=self.__title__)

    def css(self, *names):
        if "css" not in self.view_includes.keys():
            self.view_includes["css"] = ""
        for name in names:
            self.view_includes["css"] += f'<link type="text/css" rel="stylesheet" href="' \
                                         f'{self.static("css/" + name)}">\n'

    def javascript(self, *names):
        for name in names:
            self.view_includes["js"] += f'<script type="text/javascript" src="{self.static("js/" + name)}"></script>\n'

    def pagination(self, max_page, pos: int, link: str):
        self.view_includes["pagination_string"] = html_pagination(max_page, pos, link)

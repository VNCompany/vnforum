from flask import Flask, url_for, render_template
from components.pagination import html_pagination


class Controller:
    __view__ = None
    __title__ = "Page"
    view_includes = {}

    jquery_enabled = True

    def __init__(self):
        self.view_includes["css"] = ""
        self.css("main.css")
        self.view_includes["js"] = ""
        self.javascript("jquery.js", "main.js")

    @staticmethod
    def static(path: str):
        return url_for('static', filename=path)

    def view(self, **kwargs):
        if self.__view__ is None:
            raise AttributeError
        else:
            return render_template(str(self.__view__).replace(".", "/") + ".html",
                                   **kwargs,
                                   **self.view_includes,
                                   title=self.__title__)

    def css(self, *names):
        if "css" not in self.view_includes.keys():
            self.view_includes["css"] = ""
        for name in names:
            self.view_includes["css"] += f'<link rel="stylesheet" href="{self.static("css/" + name)}">\n'

    def javascript(self, *names):
        for name in names:
            self.view_includes["js"] += f'<script src="{self.static("js/" + name)}"></script>\n'

    def pagination(self, max_page, pos: int, link: str):
        self.view_includes["pagination_string"] = html_pagination(max_page, pos, link)

from flet import *
from pages.login import *
from pages.home import *
from pages.handbooks.type_home_tech import *
from pages.stats import *
from pages.requests import *

class Main(UserControl):
    def __init__(self, page:Page):
        super().__init__()
        self.page=page
        self.init_helper()
# Функция для инициализации первоначальной формы приложения
    def init_helper(self):
        self.page.on_route_change = self.on_route_change
        self.page.go('/requests')
# Фукнция для добавления новых форм и перемещения по ним
    def on_route_change(self, route):
        new_page={
            '/login': Login,
            '/home': Home,
            '/type':Type,
            '/stats': Stats,
            '/requests': Requests
        }[self.page.route](self.page)
        self.page.views.clear()
        self.page.views.append(
            View(route, [new_page])
        )
# Запуск приложения
app(target=Main)
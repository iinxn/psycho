from flet import *
from service.connection import *

class Login(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.alignment = alignment.center
        self.page.theme_mode = ThemeMode.LIGHT
        self.bgcolor=colors.DEEP_PURPLE
        self.expand=True
        
        self.login_box = Container(
            content=TextField(
                label='Логин',
            )
        )
        self.password_box = Container(
            content=TextField(
                label='Пароль',
                password=True,
                can_reveal_password=True
            )
        )
        
        self.alter_dialoge_error= AlertDialog(
            modal=True,
            title=Text('Ошибка'),
            content=Text('Вы ввели неверный логин или пароль'),
            actions=[TextButton('OK', on_click=self.cls_dialoge)],
        )
        
        self.content = Column(
            alignment='center',
            horizontal_alignment='center',
            controls=[
                Container(
                    bgcolor='white',
                    width=500,
                    padding=40,
                    border_radius=15,
                    content=Column(
                        horizontal_alignment='center',
                        controls=[
                            Container(Text(value='ООО "БытСервис"', size=18)),
                            self.login_box,
                            self.password_box,
                            ElevatedButton(
                                text='Войти',
                                bgcolor=colors.DEEP_PURPLE,
                                color='white',
                                width=500,
                                height=50,
                                on_click=self.login
                            )
                        ]
                    )
                )
            ]
        )
    def open_dialoge(self):
        self.page.dialog = self.alter_dialoge_error
        self.alter_dialoge_error.open = True
        self.page.update()

    def cls_dialoge(self, e):
        self.page.dialog = self.alter_dialoge_error
        self.alter_dialoge_error.open = False
        self.page.update()
    
    def login(self, e):
        self.page.session.clear()
        cursor = conn.cursor()
        cursor.execute('SELECT login, password, role_id FROM users;')
        users = cursor.fetchall()
        # print(users)
        for user in users:
            if self.login_box.content.value == user[0] and self.password_box.content.value == user[1]:
                self.page.session.set("role_id", user[2])
                self.page.go('/home')
                return
        self.open_dialoge()
from flet import *

class Home(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.alignment = alignment.center
        self.expand = True
        self.bgcolor = 'white'
        self.theme_mode = ThemeMode.LIGHT
        role_id = self.page.session.get('role_id')

        # Определяем все контейнеры и их кнопки
        self.containers = {
            'request_box': Container(
                content=ElevatedButton(
                    text='Заказы',
                    color='white',
                    bgcolor=colors.DEEP_PURPLE,
                    width=500,
                    height=80
                )
            ),
            'type_home_box': Container(
                content=ElevatedButton(
                    text='Вид бытовой техники',
                    color='white',
                    bgcolor=colors.DEEP_PURPLE,
                    width=500,
                    height=80
                )
            ),
            'model_home_box': Container(
                content=ElevatedButton(
                    text='Модель бытовой техники',
                    color='white',
                    bgcolor=colors.DEEP_PURPLE,
                    width=500,
                    height=80
                )
            ),
            'faults_box': Container(
                content=ElevatedButton(
                    text='Неисправности',
                    color='white',
                    bgcolor=colors.DEEP_PURPLE,
                    width=500,
                    height=80
                )
            ),
            'users_box': Container(
                content=ElevatedButton(
                    text='Пользователи',
                    color='white',
                    bgcolor=colors.DEEP_PURPLE,
                    width=500,
                    height=80
                )
            ),
            'status_box': Container(
                content=ElevatedButton(
                    text='Статусы заказов',
                    color='white',
                    bgcolor=colors.DEEP_PURPLE,
                    width=500,
                    height=80
                )
            ),
            'roles_box': Container(
                content=ElevatedButton(
                    text='Роли',
                    color='white',
                    bgcolor=colors.DEEP_PURPLE,
                    width=500,
                    height=80
                )
            ),
            'stats_box': Container(
                width=300,
                content=ElevatedButton(
                    text='Статистика',
                    color=colors.DEEP_PURPLE,
                    bgcolor='white',
                    height=50
                )
            ),
        }

        # Определяем, какие контейнеры разрешены для каждой роли
        role_permissions = {
            2: ['request_box', 'type_home_box', 'model_home_box', 'faults_box'],
            4: ['request_box'],
            3: ['request_box', 'stats_box', 'type_home_box', 'model_home_box', 'faults_box'],
            1: ['request_box', 'stats_box', 'type_home_box', 'model_home_box', 'faults_box', 'users_box', 'status_box', 'roles_box']
        }

        # Инициализируем только разрешенные контейнеры для текущей роли
        allowed_containers = role_permissions.get(role_id, [])
        for container_name in self.containers:
            if container_name not in allowed_containers:
                self.containers[container_name] = Container()  # Пустой контейнер

        # Создаем контент страницы
        self.content = Column(
            controls=[
                Container(
                    bgcolor=colors.DEEP_PURPLE,
                    width=8000,
                    padding=40,
                    content=Row(
                        spacing=10,
                        alignment='spaceBetween',
                        controls=[
                            Container(width=300),
                            Container(
                                content=Text(value='Главный экран', size=18, color='white')
                            ),
                            self.containers['stats_box'],
                        ]
                    )
                ),
                Container(
                    content=Column(
                        horizontal_alignment='center',
                        alignment='center',
                        spacing=20,
                        controls=[
                            Container(height=20),
                            self.containers['request_box'],
                            self.containers['type_home_box'],
                            self.containers['model_home_box'],
                            self.containers['faults_box'],
                            self.containers['users_box'],
                            self.containers['status_box'],
                            self.containers['roles_box']
                        ]
                    )
                )
            ]
        )

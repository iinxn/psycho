# Web Automation

Dashboard Overview The Web Automation Dashboard is a sophisticated web application designed to automate and manage various web-based tasks. Developed using Python and the Flet framework, this project aims to provide a seamless experience for automating repetitive web actions, with a robust backend supported by ClickHouse for data storage.

Features- Task Automation: Users can configure and schedule tasks for automation.

- Real-Time Monitoring: Live updates and monitoring of task execution.
- Customizable Workflows: Flexibility to create custom automation sequences.
- Performance Analytics: Detailed reports and analytics on task performance.
- User Management: Admin panel for managing user access and roles.

Technologies- Python: The core programming language used for developing the application logic.

- Flet: Employs the Flet framework for building a modern, event-driven user interface.
- ClickHouse: Utilizes ClickHouse for its high-performance analytical database capabilities.
- Docker: Leverages Docker for consistent deployment and scalability.
- Git: Implements Git for source code management and version control.

Challenges- Scalability: Ensuring the application can handle a growing number of tasks and users.

- User Experience: Balancing between advanced features and maintaining an intuitive UI.
- Data Integrity: Guaranteeing the accuracy and consistency of data throughout the application.

Future Enhancements- API Integration: Expanding the application's capabilities by integrating with various APIs.

- Machine Learning: Incorporating machine learning algorithms to optimize task automation.
- Cross-Platform Support: Developing a cross-platform application for wider accessibility.
  This project is a testament to the power of modern web technologies in creating efficient and user-friendly applications for task automation. It showcases the potential of Python and Flet in web development, while ClickHouse provides a solid foundation for data management. The use of Docker and Git further enhances the project's deployment and collaborative aspects, making it a robust solution for users and developers alike.

## Introduction

In the digital age, software applications have become essential tools for productivity, entertainment, and communication. The process of creating these applications, however, can be complex and daunting, especially for those without extensive programming experience. This project aims to simplify the software development process by providing a platform that automates many of the routine tasks involved in creating a program, making software development more accessible to a broader audience.

## Project Overview

The project, codenamed **CodeCompanion**, is a web-based application that leverages modern technologies to provide a user-friendly environment for software development. It is designed with the following objectives in mind:

- **Simplify the Development Process**: By automating repetitive tasks, CodeCompanion allows users to focus on the creative aspects of software development.
- **Educate and Guide Users**: The platform includes tutorials and guides to help users understand programming concepts and best practices.
- **Support Multiple Programming Languages**: CodeCompanion supports various programming languages, making it versatile for different types of projects.
- **Integrate with Existing Tools**: The platform works seamlessly with popular development tools and services, such as Git, Docker, and cloud-based services.

## Features

### Automated Code Generation

CodeCompanion can generate boilerplate code based on user input, significantly reducing the time required to set up a new project. Users can specify the type of application they want to create, and the platform will provide the necessary code to get started.

### Interactive Tutorials

The platform offers interactive tutorials that cover fundamental programming concepts, language syntax, and software design patterns. These tutorials are designed to be hands-on, allowing users to learn by doing.

### Drag-and-Drop Interface

For users who are not familiar with coding, CodeCompanion provides a drag-and-drop interface that lets them build software visually. This feature is particularly useful for designing user interfaces and arranging components.

### Version Control Integration

Understanding the importance of version control in software development, CodeCompanion integrates with Git to provide easy-to-use version control features directly within the platform.

### Cloud Deployment

CodeCompanion facilitates the deployment of applications to various cloud platforms. Users can deploy their applications with just a few clicks, without dealing with complex configuration files.

### Collaboration Tools

The platform includes tools that enable real-time collaboration among team members. Users can share their projects, work together on code, and communicate through integrated chat and video call features.

## Technology Stack

The project is built using the **Python** programming language and the **Flet framework**, which allows for the creation of dynamic web applications. The backend database is powered by **ClickHouse**, an efficient columnar database management system that excels at real-time query processing.

## Best Practices

CodeCompanion adheres to industry best practices in software development, including:

- **Clean Code**: The platform encourages writing clean, readable, and maintainable code.
- **Testing**: It includes tools for automated testing, ensuring that applications are reliable and bug-free.
- **Security**: Security measures are implemented throughout the platform to protect user data and applications.

## Conclusion

CodeCompanion represents a significant step forward in democratizing software development. By providing tools and resources that streamline the development process, the project empowers individuals and organizations to create software applications that meet their needs without requiring extensive technical expertise. As technology continues to evolve, CodeCompanion will adapt and incorporate new features to remain at the forefront of innovation in software development.

# Database query for this project

```SQL
ALTER TABLE status_request CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
```

## Количество выполненных заявок

```SQL
SELECT COUNT(*) AS completed_requests
FROM requests
WHERE status_id = 2;
```

## Среднее вермя выполнения заказа

```SQL
SELECT request_id, 
       DATEDIFF(date_out, date_in) AS completion_time
FROM requests
WHERE status_id = 2;
```

## Статистика по типам несиправностей

```SQL
SELECT f.name AS fault_name, 
       COUNT(r.request_id) AS request_count
FROM requests r
JOIN faults f ON r.fault_id = f.fault_id
GROUP BY r.fault_id, f.name
ORDER BY request_count DESC
```
## Вывод всей таблицы с заказами целиком
```SQL
SELECT 
    r.request_id,
    r.date_in,
    r.date_out,
    r.repair_parts,
    t.name AS type_home_name,
    m.name AS model_name,
    f.name AS fault_name,
    s.name AS status_name,
    u.full_name AS master_name,
    c.full_name AS client_name,
    com.message AS comment_message
FROM 
    requests r
LEFT JOIN 
    type_home_tech t ON r.type_home_id = t.type_home_id
LEFT JOIN 
    model_home_tech m ON r.model_id = m.model_id
LEFT JOIN 
    faults f ON r.fault_id = f.fault_id
LEFT JOIN 
    status_requests s ON r.status_id = s.status_id
LEFT JOIN 
    users u ON r.master_id = u.user_id
LEFT JOIN 
    users c ON r.client_id = c.user_id
LEFT JOIN 
    comments com ON r.comment_id = com.comment_id;
```

# ER диаграмма

![](https://i.postimg.cc/G2fpKWVd/ERD-2.png)

# Расчет количества заявок

![](https://i.postimg.cc/c1K7W0s7/vsdx.png)

# Учет заявок на ремонт бытовой техники

![](https://i.postimg.cc/YjKCK1tP/image.png)

# Forms

## main.py

```python
from flet import *
from pages.login import *
from pages.home import *
from pages.handbooks.type_home_tech import *
from pages.stats import *

class Main(UserControl):
    def __init__(self, page:Page):
        super().__init__()
        self.page=page
        self.init_helper()
# Функция для инициализации первоначальной формы приложения
    def init_helper(self):
        self.page.on_route_change = self.on_route_change
        self.page.go('/login')
# Фукнция для добавления новых форм и перемещения по ним
    def on_route_change(self, route):
        new_page={
            '/login': Login,
            '/home': Home,
            '/type':Type,
            '/stats': Stats,
        }[self.page.route](self.page)
        self.page.views.clear()
        self.page.views.append(
            View(route, [new_page])
        )
# Запуск приложения
app(target=Main)
```

## login.py

```python
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
```

## home.py

```python
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
                    height=80,
                    on_click=lambda x:x == self.page.go('/type'),
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
                    height=50,
                    on_click=lambda x:x == self.page.go('/stats')
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
```

## type_home_tech.py

```python
from flet import *
from service.connection import *

class Type(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.bgcolor = 'white'
        self.theme_mode = ThemeMode.LIGHT
      
        self.data_table = DataTable(
            columns = [
            DataColumn(Text("Код бытовой техники"), numeric=True),
            DataColumn(Text("Название")),
            ],
            rows=[],
            border=border.all(1,'black'),
            vertical_lines=border.BorderSide(1, 'black'),
            horizontal_lines=border.BorderSide(1,'black'),
        )
      
        self.add_new_box = Container(
            content=TextField(
                label='Поле ввода',
                width=200
            )
        )
      
        self.alter_dialoge_message = AlertDialog(
            title=Text("Информация"),
            content=Text("Данные были успешно добавлены в таблицу"),
            actions=[TextButton('OK', on_click=self.cls_dlg)],
        )
      
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
                            Container(
                                width=300,
                                content=Row(
                                    controls=[
                                        IconButton(
                                            icon=icons.ARROW_BACK,
                                            icon_color=colors.DEEP_PURPLE,
                                            bgcolor='white',
                                            width=60,
                                            height=60,
                                            on_click=lambda x: x == self.page.go('/home')
                                        )
                                    ]
                                )
                            ),
                            Container(
                                content=Text(value='Вид бытовой техники', size=18, color='white')
                            ),
                            Container(width=300)
                        ]
                    )
                ),
                Container(
                    content=Row(
                        alignment='center',
                        spacing=20,
                        controls=[
                            Container(height=20),
                            self.add_new_box,
                            Container(
                                content=ElevatedButton(
                                    text='Добавить',
                                    color='white',
                                    bgcolor=colors.DEEP_PURPLE,
                                    width=200,
                                    height=50,
                                    on_click=self.insert_new
                                )
                            )
                        ]
                    )
                ),
                Container(
                    content=self.data_table,
                    alignment=alignment.center,
                    padding=40
                )
            ]
        )
        self.show_type_home_tech()
    def show_type_home_tech(self):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM type_home_tech;")
        results = cursor.fetchall()
        data_rows = []
        for row in results:
            cells = [DataCell(Text(str(value))) for value in row]
            data_row = DataRow(cells=cells)
            data_rows.append(data_row)
        self.data_table.rows = data_rows
        self.page.update()
  
  
    def cls_dlg(self,e):
        self.page.dialog = self.alter_dialoge_message
        self.alter_dialoge_message.open = False
        self.page.update()
  
    def insert_new(self,e):
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO type_home_tech(name) VALUES ('{self.add_new_box.content.value}')")
        conn.commit()
        self.add_new_box.content.value = ''
        self.show_type_home_tech()
```

## stats.py

```python
from flet import *
from service.connection import *

class Stats(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.bgcolor = 'white'
        self.theme_mode = ThemeMode.LIGHT
      
        self.data_table = DataTable(
            columns = [],
            rows=[],
            border=border.all(1,'black'),
            vertical_lines=border.BorderSide(1, 'black'),
            horizontal_lines=border.BorderSide(1,'black'),
        )
      
        self.dp_options = Container(
            content=Dropdown(
                width=500,
                label='Шаблон',
                options=[
                    dropdown.Option('Количество выполненных заказов'),
                    dropdown.Option('Среднее время выполнения заявки'),
                    dropdown.Option('Статистика по типам неисправностей'),
                ]
            )
        )
      
        self.alter_dialoge_message = AlertDialog(
            title=Text("Предупреждение"),
            content=Text("Вы не выбрали шаблон"),
            actions=[TextButton('OK', on_click=self.cls_dlg)],
        )
      
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
                            Container(
                                width=300,
                                content=Row(
                                    controls=[
                                        IconButton(
                                            icon=icons.ARROW_BACK,
                                            icon_color=colors.DEEP_PURPLE,
                                            bgcolor='white',
                                            width=60,
                                            height=60,
                                            on_click=lambda x: x == self.page.go('/home')
                                        )
                                    ]
                                )
                            ),
                            Container(
                                content=Text(value='Статистика', size=18, color='white')
                            ),
                            Container(width=300)
                        ]
                    )
                ),
                Container(
                    content=Row(
                        alignment='center',
                        spacing=20,
                        controls=[
                            Container(height=20),
                            self.dp_options,
                            Container(
                                content=ElevatedButton(
                                    text='Сформировать',
                                    color='white',
                                    bgcolor=colors.DEEP_PURPLE,
                                    width=200,
                                    height=50,
                                    on_click=self.generate_stats
                                )
                            )
                        ]
                    )
                ),
                Container(
                    content=self.data_table,
                    alignment=alignment.center,
                    padding=40
                )
            ]
        )
    def cls_dlg(self,e):
        self.page.dialog = self.alter_dialoge_message
        self.alter_dialoge_message.open = False
        self.page.update()
  
    def generate_stats(self,e):
        if self.dp_options.content.value == 'Количество выполненных заказов':
            self.count_complete_requests()
        elif self.dp_options.content.value == 'Среднее время выполнения заявки':
            self.avg_time_complete_requests()
        elif self.dp_options.content.value == 'Статистика по типам неисправностей':
            self.fault_stats()
        else:
            self.page.dialog = self.alter_dialoge_message
            self.alter_dialoge_message.open = True
            self.page.update()
  
    def count_complete_requests(self):
        cursor = conn.cursor()
        cursor.execute("""
        SELECT COUNT(*) AS completed_requests
        FROM requests
        WHERE status_id = 2;
        """)
        results = cursor.fetchall()
        data_columns = [
            DataColumn(Text("Количество выполненных заказа"), numeric=True),
        ]
        data_rows = []
        for row in results:
            cells = [DataCell(Text(str(value))) for value in row]
            data_row = DataRow(cells=cells)
            data_rows.append(data_row)
        self.data_table.columns = data_columns
        self.data_table.rows = data_rows
        self.page.update()
  
    def avg_time_complete_requests(self):
        cursor = conn.cursor()
        cursor.execute("""
        SELECT request_id, 
            DATEDIFF(date_out, date_in) AS completion_time
        FROM requests
        WHERE status_id = 2;
        """)
        results = cursor.fetchall()
        data_columns = [
            DataColumn(Text("Код заказа"), numeric=True),
            DataColumn(Text("Среднее время выполнения заказа"), numeric=True),
        ]
        data_rows = []
        for row in results:
            cells = [DataCell(Text(str(value))) for value in row]
            data_row = DataRow(cells=cells)
            data_rows.append(data_row)
        self.data_table.columns = data_columns
        self.data_table.rows = data_rows
        self.page.update()
  
    def fault_stats(self):
        cursor = conn.cursor()
        cursor.execute("""
        SELECT f.name AS fault_name, 
            COUNT(r.request_id) AS request_count
        FROM requests r
        JOIN faults f ON r.fault_id = f.fault_id
        GROUP BY r.fault_id, f.name
        ORDER BY request_count DESC
        """)
        results = cursor.fetchall()
        data_columns = [
            DataColumn(Text("Название неисправности")),
            DataColumn(Text("Количество в заказах"), numeric=True),
        ]
        data_rows = []
        for row in results:
            cells = [DataCell(Text(str(value))) for value in row]
            data_row = DataRow(cells=cells)
            data_rows.append(data_row)
        self.data_table.columns = data_columns
        self.data_table.rows = data_rows
        self.page.update()
```

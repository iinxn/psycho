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
## request.py
```python
from flet import *
from service.connection import *

class Requests(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.bgcolor = 'white'
        self.theme_mode = ThemeMode.LIGHT
        
        self.data_table = DataTable(
            columns = [
            DataColumn(Text("Код заказа"), numeric=True),
            DataColumn(Text("Дата приемки")),
            DataColumn(Text("Дата окончания")),
            DataColumn(Text("Запчасти на ремонт")),
            DataColumn(Text("Вид")),
            DataColumn(Text("Модель")),
            DataColumn(Text("Неисправность")),
            DataColumn(Text("Статус заказа")),
            DataColumn(Text("Мастер")),
            DataColumn(Text("Клиент")),
            ],
            rows=[],
            border=border.all(1,'black'),
            vertical_lines=border.BorderSide(1, 'black'),
            horizontal_lines=border.BorderSide(1,'black'),
        )
        
        self.search = Container(
            content=TextField(
                label='Поиск',
                width=200,
                # on_change=self.search_in_requests
            )
        )
        
        self.alter_dialoge_message = AlertDialog(
            title=Text("Информация"),
            content=Text("Данные были успешно добавлены в таблицу"),
            actions=[TextButton('OK', on_click=self.cls_dlg)],
        )
        
        self.alter_dialoge_data = AlertDialog(
            content='',
            actions=[TextButton('OK', on_click=self.cls_dlg)]
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
                                content=Text(value='Заказы', size=18, color='white')
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
                            self.search,
                            Container(
                                content=ElevatedButton(
                                    text='Добавить',
                                    color='white',
                                    bgcolor=colors.DEEP_PURPLE,
                                    width=200,
                                    height=50,
                                    on_click=self.open_alter_dialoge_data
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
        cursor.execute("""
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
        """)
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
        
        self.page.dialog = self.alter_dialoge_data
        self.alter_dialoge_data.open = False
        
        self.page.update()
    
    def open_alter_dialoge_data(self,e):
        self.page.dialog = self.alter_dialoge_data
        self.alter_dialoge_data.title = Text('Добавление нового заказа')
        self.alter_dialoge_data.open = True
        self.page.update()
```

# Example to make dropdown events
```python
from flet import *
from utils.consts import primary_colors 
from utils.components import *
from service.connection import *

class Add(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.theme_mode = ThemeMode.LIGHT
        self.alignment = alignment.center
        self.components_manager = Components(page)
        self.expand = True
        self.bgcolor = primary_colors['WHITE']
        self.selected_rows = set()
        self.data_table = DataTable(
            columns=[
                DataColumn(Text("""
                                Код
                                показателя"""), numeric=True),
                DataColumn(Text("""
                                Код
                                ед. из."""), numeric=True),
                DataColumn(Text("Наименование")),
                DataColumn(Text("Редактирование")),
            ],
            rows=[],  # Leave this empty for now
            border=border.all(1, primary_colors['BLACK']),
            vertical_lines=border.BorderSide(1, primary_colors['BLACK']),
            horizontal_lines=border.BorderSide(1, primary_colors['BLACK']),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=colors.BLACK12,
            heading_row_height=100,
            width=2000,
            data_row_max_height=100
        )
        
        self.dropdown_options_specialists = []
        self.dropdown_options_specialists_alter_dialoge = []
        dropdown_options_units_1 = []
        dropdown_options_units_2 = []
        dropdown_options_departments = []
        
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM name_of_department ORDER BY department_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_departments.append(dropdown.Option(row[0]))

        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
        
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT type FROM units_of_measurement ORDER BY measurement_id')
            results = cursor.fetchall()

            for row in results:
                dropdown_options_units_1.append(dropdown.Option(row[0]))
                dropdown_options_units_2.append(dropdown.Option(row[0]))
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
        
#*TEXTFIELD
        self.add_textfield_box = Container(
          content=TextField(
            hint_style=TextStyle(
              size=12, color=primary_colors['MANATEE']
            ),
            label='Поле ввода',
            cursor_color=primary_colors['MANATEE'],
            text_style=TextStyle(
              size=14,
              color=primary_colors['GREEN'],
            ),
          )
        )
        self.name_of_department_menu_box = Container(
            content=Dropdown(
                hint_text='Выберите управление',
                color=primary_colors['BLACK'],
                width=500,
                options=dropdown_options_departments,
                on_change=self.show_specialists
            ),
        )
        self.cb_units = Container(
          content=Dropdown(
                hint_text='Выберите измерения',
                color=primary_colors['BLACK'],
                width=230,
                options=dropdown_options_units_1,  # Set the options from the fetched data
            ),
        )
        self.dp_units = Container(
          content=Dropdown(
                hint_text='Выберите измерения',
                color=primary_colors['BLACK'],
                width=300,
                options=dropdown_options_units_2,  # Set the options from the fetched data
            ),
        )
        
        self.edit_name = Container(
          content=TextField(
                    hint_style=TextStyle(
                        size=12, color=primary_colors['MANATEE']
                    ),
                    label='Введите другое название',
                    cursor_color=primary_colors['MANATEE'],
                    text_style=TextStyle(
                        size=14,
                        color=primary_colors['GREEN'],
                    ),
                        ),
        )
        
        self.specialist_menu_box = Container(
            content=Dropdown(
                hint_text='Выберите специалиста',
                color=primary_colors['BLACK'],
                width=330,
                options=self.dropdown_options_specialists,
            )
        )
        self.specialist_menu_box_alter_dialoge = Container(
            content=Dropdown(
                hint_text='Выберите специалиста',
                color=primary_colors['BLACK'],
                width=330,
                options=self.dropdown_options_specialists_alter_dialoge,
            )
        )
        
        self.alter_dialog_add_new_specialists = AlertDialog(
            modal=True,
            title=Text("Изменить строку"),
            content=Column(
              height=250,
              width=500,
              controls=[
                self.dp_units,
                self.edit_name,
                self.specialist_menu_box_alter_dialoge
              ]
            ),
            actions=[
                TextButton("Изменить", on_click=self.edit_name_in_table),
                TextButton("Закрыть", on_click=self.close_edit_dialog),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

#*HEADER
        self.content = ListView(
            spacing=0,
            # scroll=ScrollMode.ADAPTIVE,
            controls=[
                Container(
                    width=8000,
                    padding=40,
                    bgcolor=primary_colors['GREEN'],
                    # border_radius=15,
                    content=Column(
                        horizontal_alignment='center',  # Align the text to the right
                        controls=[
                          Container(
                            # alignment='center',
                            content=Row(
                              alignment='spaceBetween',
                              controls=[
                                Container(
                                  width=200,
                                  content=Row(
                                    spacing=10,
                                    controls=[
                                      Container(
                                          bgcolor=primary_colors['WHITE'],
                                          width=70,
                                          height=70,
                                          border_radius=50,
                                          content=IconButton(
                                              icons.ARROW_BACK_OUTLINED,
                                              icon_color=primary_colors['GREEN'],
                                              icon_size=30,
                                              on_click=lambda x: x == self.page.go('/handbook')
                                          )
                                      ),
                                      Container(
                                          bgcolor=primary_colors['WHITE'],
                                          width=70,
                                          height=70,
                                          border_radius=50,
                                          content=IconButton(
                                              icons.HOME,
                                              icon_color=primary_colors['GREEN'],
                                              icon_size=30,
                                              on_click=lambda x: x == self.page.go('/home')
                                          )
                                      ),
                                    ]
                                  )
                                ),
                                Container(
                                    content=Text(
                                    value='Добавление показателя в справочник',
                                    size=18,
                                    color=primary_colors['WHITE'],
                                    text_align='center',
                                  ),
                                ),
                                Container(width=70),
                              ]
                            )
                          )
                            
                            
                            
                        ],
                    )
                ),
                
#*MANUAL BUTTONS
                Container(
                    expand=True,
                    bgcolor=primary_colors['WHITE'],
                    content=Column(
                      expand=True,
                      # alignment='center',
                      horizontal_alignment='center',
                      controls=[
#*1ST ROW
                          Container(height=20),
                          Container(
                            Row(
                              spacing='50',
                              alignment='center',
                              controls=[
                                self.name_of_department_menu_box,
                                self.specialist_menu_box,
                                ElevatedButton(
                                  color=primary_colors['WHITE'],
                                  bgcolor=primary_colors['GREEN'],
                                  width=200,
                                  height=70,
                                  content=Column(
                                      horizontal_alignment='center',
                                      alignment='center',
                                      controls=[
                                          Container(
                                              Text(
                                                  value='Сформировать',
                                                  size=16,
                                                  color=primary_colors['WHITE'],
                                                  text_align='center',
                                                  weight='bold',
                                              )
                                          )
                                      ]
                                  ),
                                  on_click=self.show_indicators,
                                ),
                              ]
                            )
                          ),
                          Container(
                            Row(
                              spacing='50',
                              alignment='center',
                              controls=[
                                  # Container(width=90),
                                  
                                  self.add_textfield_box,
                                  self.cb_units,
                                  ElevatedButton(
                                    color=primary_colors['WHITE'],
                                    bgcolor=primary_colors['GREEN'],
                                    width=200,
                                    height=70,
                                    content=Column(
                                        horizontal_alignment='center',
                                        alignment='center',
                                        controls=[
                                            Container(
                                                Text(
                                                    value='Добавить',
                                                    size=16,
                                                    color=primary_colors['WHITE'],
                                                    text_align='center',
                                                    weight='bold',
                                                )
                                            )
                                        ]
                                    ),
                                    on_click=self.insert_into_db,
                                  ),
                                  ElevatedButton(
                                      color=primary_colors['WHITE'],
                                      bgcolor=primary_colors['GREEN'],
                                      width=200,
                                      height=70,
                                      content=Column(
                                          horizontal_alignment='center',
                                          alignment='center',
                                          controls=[
                                              Container(
                                                  Text(
                                                      value='Редактировать',
                                                      size=16,
                                                      color=primary_colors['WHITE'],
                                                      text_align='center',
                                                      weight='bold',
                                                  )
                                              )
                                          ]
                                      ),
                                      on_click=self.show_edit_dialog,
                                  ),
                                  ElevatedButton(
                                      color=primary_colors['WHITE'],
                                      bgcolor=primary_colors['GREEN'],
                                      width=200,
                                      height=70,
                                      content=Column(
                                          horizontal_alignment='center',
                                          alignment='center',
                                          controls=[
                                              Container(
                                                  Text(
                                                      value='Удалить',
                                                      size=16,
                                                      color=primary_colors['WHITE'],
                                                      text_align='center',
                                                      weight='bold',
                                                  )
                                              )
                                          ]
                                      ),
                                      on_click=self.delete_indicators,
                                  ),
                              ]
                            )
                          ), 
                          
                          # Container(height=50),
#*2ND ROW (DATATABLE)
                          Container(
                            content=self.data_table,
                            alignment=alignment.center,
                            padding=padding.all(20),
                          ),
                          Container(height=50),
                          #4th row
                          
                      ],
                  )
                ),
            ]
        )
#*DB CONNECTIONS WITH SELECT QUERY
    def show_specialists(self, e):
      self.dropdown_options_specialists.clear()
      try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT department_id FROM name_of_department WHERE name = '{self.name_of_department_menu_box.content.value}'")
        specialist_department_id = cursor.fetchone()[0]
        
        cursor.execute(f"SELECT full_name FROM specialists WHERE specialist_department_id = {specialist_department_id}")
        specialists_full_name = cursor.fetchall()

        for row in specialists_full_name:
            self.dropdown_options_specialists.append(dropdown.Option(row[0]))
            self.dropdown_options_specialists_alter_dialoge.append(dropdown.Option(row[0]))
            
        self.page.update()
      except Exception as e:
          print(f"Error fetching data from the database: {str(e)}")

    def show_indicators(self, e): 
      try:
        cursor = connection.cursor()
        sql_select_specialist_id = "SELECT specialist_id FROM specialists WHERE full_name = '{}'".format(self.specialist_menu_box.content.value)
        cursor.execute(sql_select_specialist_id)
        specialist_id = cursor.fetchone()[0]
        query_select = '''
        SELECT
            ni.indicators_id,
            um.type,
            ni.name,
        FROM name_of_indicators AS ni
        JOIN units_of_measurement AS um ON ni.measurement_id = um.measurement_id
        WHERE specialist_id = {}
        ORDER BY ni.indicators_id;
        '''.format(specialist_id)
        cursor.execute(query_select)
        results = cursor.fetchall()
        query_result = results
        if not query_result:
          self.components_manager.show_block_dialog("У пользователя нет заполненных показателей", "Информация")
        else:
          data_rows = []
          for row in query_result:
              cells = [DataCell(Text(str(value))) for value in row]
              data_row = DataRow(cells=cells)
              checkbox = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
              cells.append(DataCell(checkbox))
              data_rows.append(data_row)
          self.data_table.rows = data_rows
          self.selected_rows.clear()
          self.page.dialog = self.alter_dialog_add_new_specialists
          self.alter_dialog_add_new_specialists.open = False
          self.page.update()
      except:
        self.components_manager.show_block_dialog("Вы не выбрали управление или специалиста", "Ошибка")

    def insert_into_db(self, e):
      selected_unit = self.cb_units.content.value
      if self.add_textfield_box.content.value == "" or selected_unit == "" or self.specialist_menu_box.content.value == "":
        self.components_manager.show_block_dialog("Вы не заполнили все поля", "Ошибка")
      else:
        try:
          cursor = connection.cursor()
          sql_select_specialist_id = "SELECT specialist_id FROM specialists WHERE full_name = '{}'".format(self.specialist_menu_box.content.value)
          cursor.execute(sql_select_specialist_id)
          specialist_id = cursor.fetchone()[0]
          cursor.execute(f"SELECT measurement_id FROM units_of_measurement WHERE type = '{selected_unit}'")
          units_id = cursor.fetchone()[0]
          cursor.execute("SELECT max(indicators_id) FROM name_of_indicators;")
          max_id = cursor.fetchone()[0]
          query = "INSERT INTO TABLE name_of_indicators (indicators_id, measurement_id, name, specialist_id) VALUES ({}+1,{},'{}',{})".format(int(max_id), units_id, self.add_textfield_box.content.value, int(specialist_id))
          cursor.execute(query)
          print("Запись успешно добавлена в базу данных")
          query_select = '''
          SELECT
              ni.indicators_id,
              um.type,
              ni.name,
          FROM name_of_indicators AS ni
          JOIN units_of_measurement AS um ON ni.measurement_id = um.measurement_id
          WHERE specialist_id = {}
          ORDER BY ni.indicators_id;
          '''.format(specialist_id)
          cursor.execute(query_select)
          results = cursor.fetchall()
          query_result = results
          data_rows = []
          for row in query_result:
              cells = [DataCell(Text(str(value))) for value in row]
              data_row = DataRow(cells=cells)
              checkbox = Checkbox(value=False, on_change=lambda e, row=row: self.toggle_row_selection(e, row))
              cells.append(DataCell(checkbox))
              data_rows.append(data_row)
          self.data_table.rows = data_rows
          self.add_textfield_box.content.value = ""
          self.cb_units.content.value = ""
          self.page.update()
        except Exception as e:
          self.components_manager.show_block_dialog("Ошибка при добавлении записи в базу данных", "Ошибка")
          print(f"Ошибка при добавлении записи в базу данных: {str(e)}")

    def toggle_row_selection(self, e, row):
        if row not in self.selected_rows:
            self.selected_rows.add(row)
        else:
            self.selected_rows.remove(row)

    def show_edit_dialog(self, e):
        if not self.selected_rows:
            self.components_manager.show_block_dialog("Вы не выбрали строку в таблице", "Ошибка")
        else:
            selected_row = next(iter(self.selected_rows))
            selected_data = selected_row[2]
            self.edit_name.content.value = selected_data
            self.dp_units.content.value = selected_row[1]
            self.specialist_menu_box_alter_dialoge.content.value = self.specialist_menu_box.content.value
            self.page.dialog = self.alter_dialog_add_new_specialists
            self.alter_dialog_add_new_specialists.open = True
            self.page.update()


    def edit_name_in_table(self, e):
        selected_row = next(iter(self.selected_rows))
        cursor = connection.cursor()
        sql_select_specialist_id = "SELECT specialist_id FROM specialists WHERE full_name = '{}'".format(self.specialist_menu_box.content.value)
        cursor.execute(sql_select_specialist_id)
        specialist_id = cursor.fetchone()[0]
        cursor.execute(f"SELECT measurement_id FROM units_of_measurement WHERE type = '{self.dp_units.content.value}'")
        units_id = cursor.fetchone()[0]
        sql_select_specialist_id_alter_dialoge = "SELECT specialist_id FROM specialists WHERE full_name = '{}'".format(self.specialist_menu_box_alter_dialoge.content.value)
        cursor.execute(sql_select_specialist_id_alter_dialoge)
        specialist_id_alter_dialoge = cursor.fetchone()[0]
        print(specialist_id_alter_dialoge)
        if self.edit_name.content.value != selected_row[2]:
            query_name = "ALTER TABLE name_of_indicators UPDATE name = '{}' WHERE indicators_id = {}".format(self.edit_name.content.value, selected_row[0])
            print(query_name)
            cursor.execute(query_name)
            self.show_indicators(e)
        elif self.dp_units.content.value != selected_row[1]:
            query_units = "ALTER TABLE name_of_indicators UPDATE measurement_id = {} WHERE indicators_id = {}".format(int(units_id), selected_row[0])
            print(query_units)
            cursor.execute(query_units)
            self.show_indicators(e)
        elif self.specialist_menu_box_alter_dialoge.content.value != self.specialist_menu_box.content.value:
            query_specialist = "ALTER TABLE name_of_indicators UPDATE specialist_id = {} WHERE indicators_id = {}".format(int(specialist_id_alter_dialoge), selected_row[0])
            print(query_specialist)
            cursor.execute(query_specialist)
            self.show_indicators(e)
        else:
            self.components_manager.show_block_dialog("Предупреждение","Изменений не было обнаружено")

    def close_edit_dialog(self, e):
        self.page.dialog = self.alter_dialog_add_new_specialists
        self.alter_dialog_add_new_specialists.open = False
        self.page.update()

    def delete_indicators(self, e):
      if not self.selected_rows:
            self.components_manager.show_block_dialog("Вы не выбрали строку в таблице", "Ошибка")
      else:
        cursor = connection.cursor()
        for selected_row in self.selected_rows:
            query_delete_department = f"DELETE FROM name_of_indicators WHERE indicators_id = {selected_row[0]}"
            cursor.execute(query_delete_department)
            connection.commit()
            print(query_delete_department)
        self.show_indicators(e)
        self.selected_rows.clear()
        self.components_manager.show_block_dialog("Запись удалена", "Успешно")
        self.page.update()
```
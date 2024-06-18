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
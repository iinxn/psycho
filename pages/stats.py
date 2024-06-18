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
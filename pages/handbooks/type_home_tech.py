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
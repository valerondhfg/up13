# -*- coding: utf-8 -*-

import sys
import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit

# Импорт сгенерированных интерфейсов
from login_ui import Ui_MainWindow as LoginUi  # Интерфейс окна авторизации
from main_ui import MainWindow as MainUi      # Интерфейс главного окна

# Глобальные переменные для хранения роли и данных пользователя
role = 'Гость'      # Роль пользователя (Администратор, Менеджер, Гость)
fio = ''            # ФИО пользователя
login = ''          # Логин пользователя

#ФУНКЦИЯ СОЗДАНИЯ БАЗЫ ДАННЫХ
def create_db():
    """Создает базу данных и таблицы, если их нет, и заполняет тестовыми данными"""
    conn = sqlite3.connect('linda.sqlite')  # Подключение к БД
    cursor = conn.cursor()
    
    # Создание таблицы продуктов (мебельные гарнитуры)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            type VARCHAR(20) NOT NULL,
            country VARCHAR(50) NOT NULL,
            items_count INTEGER NOT NULL,
            material VARCHAR(50) NOT NULL,
            upholstery VARCHAR(50),
            price DECIMAL(12,2) NOT NULL
        )
    ''')
    
    # Создание таблицы клиентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name VARCHAR(50) NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            middle_name VARCHAR(50),
            address VARCHAR(255) NOT NULL,
            city VARCHAR(50) NOT NULL
        )
    ''')
    
    # Создание таблицы заказов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            order_number TEXT NOT NULL UNIQUE
        )
    ''')
    
    # Добавление тестовых данных, если таблицы пустые
    cursor.execute("SELECT COUNT(*) FROM Products")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Products (name, type, country, items_count, material, upholstery, price) VALUES ('Спальня Комфорт', 'спальный', 'Россия', 5, 'ДСП', 'Ткань', 45000)")
        cursor.execute("INSERT INTO Products (name, type, country, items_count, material, upholstery, price) VALUES ('Кухня Стандарт', 'кухонный', 'Италия', 8, 'МДФ', NULL, 68000)")
        cursor.execute("INSERT INTO Products (name, type, country, items_count, material, upholstery, price) VALUES ('Спальня Люкс', 'спальный', 'Германия', 7, 'Массив', 'Велюр', 120000)")
    
    cursor.execute("SELECT COUNT(*) FROM Clients")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Clients (last_name, first_name, middle_name, address, city) VALUES ('Иванов', 'Иван', 'Иванович', 'ул. Ленина, д.1', 'Москва')")
        cursor.execute("INSERT INTO Clients (last_name, first_name, middle_name, address, city) VALUES ('Петрова', 'Елена', 'Сергеевна', 'пр. Мира, 15', 'Санкт-Петербург')")
        cursor.execute("INSERT INTO Clients (last_name, first_name, middle_name, address, city) VALUES ('Сидоров', 'Алексей', 'Петрович', 'ул. Гагарина, 23', 'Казань')")
    
    cursor.execute("SELECT COUNT(*) FROM Orders")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Orders (client_id, product_id, order_date, order_number) VALUES (1, 1, '2025-03-01', 'ORD-001')")
        cursor.execute("INSERT INTO Orders (client_id, product_id, order_date, order_number) VALUES (2, 2, '2025-03-05', 'ORD-002')")
        cursor.execute("INSERT INTO Orders (client_id, product_id, order_date, order_number) VALUES (3, 3, '2025-03-10', 'ORD-003')")
    
    conn.commit()   # Сохраняем изменения
    conn.close()    # Закрываем соединение

#
class LoginWindow(QtWidgets.QMainWindow):
    """Класс окна авторизации"""
    def __init__(self):
        super().__init__()
        self.ui = LoginUi()                     # Загружаем интерфейс
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.check_login)  # Кнопка "Войти"
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)  # Скрытие пароля
        self.users = {"admin": ("Администратор", "admin"), "manager": ("Менеджер", "manager")}  # Данные пользователей
    
    def check_login(self):
        """Проверка введенных логина и пароля"""
        global role, fio, login
        login = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        
        # Проверяем, есть ли пользователь в словаре
        if login in self.users and self.users[login][1] == password:
            role = self.users[login][0]         # Устанавливаем роль
            fio = login
            QMessageBox.information(self, 'Успех', f'Вы вошли как {role}')
            self.close()                        # Закрываем окно авторизации
            main_win.set_roles(role, fio)       # Передаем роль в главное окно
            main_win.show()                     # Показываем главное окно
        else:
            # Если логин/пароль неверные - вход как гость
            role = 'Гость'
            fio = 'Гость'
            QMessageBox.warning(self, 'Ошибка', 'Вы вошли как Гость')
            self.close()
            main_win.set_roles(role, fio)
            main_win.show()


class ProductDialog(QDialog):
    """Диалоговое окно для добавления/редактирования товара"""
    def __init__(self, parent=None, record=None):
        super().__init__(parent)
        self.setWindowTitle("Товар")
        self.setModal(True)                     # Модальное окно (блокирует главное)
        layout = QVBoxLayout()
        
        # Создаем поля ввода
        self.edit_name = QLineEdit()            # Название
        self.edit_type = QComboBox()            # Тип (выпадающий список)
        self.edit_type.addItems(["спальный", "кухонный"])
        self.edit_country = QLineEdit()         # Страна
        self.spin_items = QSpinBox()            # Количество предметов
        self.spin_items.setMinimum(1)
        self.edit_material = QLineEdit()        # Материал
        self.edit_upholstery = QLineEdit()      # Обивка
        self.double_price = QDoubleSpinBox()    # Цена
        self.double_price.setMaximum(9999999.99)
        
        # Добавляем виджеты на форму
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.edit_name)
        layout.addWidget(QLabel("Тип:"))
        layout.addWidget(self.edit_type)
        layout.addWidget(QLabel("Страна:"))
        layout.addWidget(self.edit_country)
        layout.addWidget(QLabel("Количество:"))
        layout.addWidget(self.spin_items)
        layout.addWidget(QLabel("Материал:"))
        layout.addWidget(self.edit_material)
        layout.addWidget(QLabel("Обивка:"))
        layout.addWidget(self.edit_upholstery)
        layout.addWidget(QLabel("Цена:"))
        layout.addWidget(self.double_price)
        
        # Кнопки OK/Cancel
        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
        self.setLayout(layout)
        
        # Если передана запись для редактирования - заполняем поля
        if record:
            self.edit_name.setText(record[1])
            self.edit_type.setCurrentText(record[2])
            self.edit_country.setText(record[3])
            self.spin_items.setValue(record[4])
            self.edit_material.setText(record[5])
            if record[6]:
                self.edit_upholstery.setText(record[6])
            self.double_price.setValue(record[7])
    
    def get_data(self):
        """Возвращает данные из полей ввода"""
        return (self.edit_name.text(), self.edit_type.currentText(), self.edit_country.text(),
                self.spin_items.value(), self.edit_material.text(),
                self.edit_upholstery.text() if self.edit_upholstery.text() else None, self.double_price.value())


class ClientDialog(QDialog):
    """Диалоговое окно для добавления/редактирования клиента"""
    def __init__(self, parent=None, record=None):
        super().__init__(parent)
        self.setWindowTitle("Клиент")
        self.setModal(True)
        layout = QVBoxLayout()
        
        # Поля ввода данных клиента
        self.edit_last = QLineEdit()        # Фамилия
        self.edit_first = QLineEdit()       # Имя
        self.edit_middle = QLineEdit()      # Отчество
        self.edit_address = QLineEdit()     # Адрес
        self.edit_city = QLineEdit()        # Город
        
        layout.addWidget(QLabel("Фамилия:"))
        layout.addWidget(self.edit_last)
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.edit_first)
        layout.addWidget(QLabel("Отчество:"))
        layout.addWidget(self.edit_middle)
        layout.addWidget(QLabel("Адрес:"))
        layout.addWidget(self.edit_address)
        layout.addWidget(QLabel("Город:"))
        layout.addWidget(self.edit_city)
        
        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
        self.setLayout(layout)
        
        if record:
            self.edit_last.setText(record[1])
            self.edit_first.setText(record[2])
            self.edit_middle.setText(record[3] if record[3] else "")
            self.edit_address.setText(record[4])
            self.edit_city.setText(record[5])
    
    def get_data(self):
        return (self.edit_last.text(), self.edit_first.text(),
                self.edit_middle.text() if self.edit_middle.text() else None,
                self.edit_address.text(), self.edit_city.text())


class OrderDialog(QDialog):
    """Диалоговое окно для добавления/редактирования заказа"""
    def __init__(self, parent=None, record=None):
        super().__init__(parent)
        self.setWindowTitle("Заказ")
        self.setModal(True)
        layout = QVBoxLayout()
        
        # Загружаем списки клиентов и товаров из БД
        conn = sqlite3.connect('linda.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT client_id, last_name || ' ' || first_name FROM Clients")
        self.clients = cursor.fetchall()
        cursor.execute("SELECT product_id, name FROM Products")
        self.products = cursor.fetchall()
        conn.close()
        
        # Выпадающие списки для выбора клиента и товара
        self.combo_client = QComboBox()
        for c in self.clients:
            self.combo_client.addItem(c[1], c[0])
        self.combo_product = QComboBox()
        for p in self.products:
            self.combo_product.addItem(p[1], p[0])
        
        self.date_edit = QDateEdit()                # Дата заказа
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.edit_number = QLineEdit()              # Номер заказа
        
        layout.addWidget(QLabel("Клиент:"))
        layout.addWidget(self.combo_client)
        layout.addWidget(QLabel("Товар:"))
        layout.addWidget(self.combo_product)
        layout.addWidget(QLabel("Дата:"))
        layout.addWidget(self.date_edit)
        layout.addWidget(QLabel("Номер заказа:"))
        layout.addWidget(self.edit_number)
        
        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
        self.setLayout(layout)
        
        # Если редактируем - заполняем поля
        if record:
            idx = self.combo_client.findData(record[1])
            if idx >= 0:
                self.combo_client.setCurrentIndex(idx)
            idx = self.combo_product.findData(record[2])
            if idx >= 0:
                self.combo_product.setCurrentIndex(idx)
            self.date_edit.setDate(QDate.fromString(record[3], "yyyy-MM-dd"))
            self.edit_number.setText(record[4])
    
    def get_data(self):
        return (self.combo_client.currentData(), self.combo_product.currentData(),
                self.date_edit.date().toString("yyyy-MM-dd"), self.edit_number.text())

# ГЛАВНОЕ ОКНО
class MainWindow(QtWidgets.QMainWindow):
    """Главное окно программы"""
    def __init__(self):
        super().__init__()
        self.ui = MainUi()
        self.ui.setupUi(self)
        
        # Выпадающий список для выбора таблицы (размещаем в меню)
        self.table_selector = QtWidgets.QComboBox()
        self.table_selector.addItems(["Продукты", "Клиенты", "Заказы"])
        self.ui.menubar.setCornerWidget(self.table_selector)
        self.table_selector.currentTextChanged.connect(self.load_table)
        
        # Подключение кнопок к функциям
        self.ui.pushButton.clicked.connect(self.add_record)      # Добавить
        self.ui.pushButton_2.clicked.connect(self.delete_record) # Удалить
        self.ui.pushButton_3.clicked.connect(self.edit_record)   # Редактировать
        self.ui.pushButton_4.clicked.connect(self.close)         # Выход
        
        # Подключение пунктов меню "Справка"
        self.ui.action.triggered.connect(self.show_about)        # Об авторе
        self.ui.action_2.triggered.connect(self.show_guide)      # Руководство
        
        self.current_table = None
        self.load_table("Продукты")  # Загружаем таблицу продуктов по умолчанию
    
    def set_roles(self, role, fio):
        """Настройка прав доступа в зависимости от роли пользователя"""
        self.ui.label_2.setText(f"{fio} ({role})")  # Отображаем роль на форме
        
        # Включаем/отключаем кнопки в зависимости от роли
        if role == "Администратор":
            self.ui.pushButton.setEnabled(True)   # Добавление разрешено
            self.ui.pushButton_2.setEnabled(True) # Удаление разрешено
            self.ui.pushButton_3.setEnabled(True) # Редактирование разрешено
        elif role == "Менеджер":
            self.ui.pushButton.setEnabled(True)   # Только добавление
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
        else:  # Гость
            self.ui.pushButton.setEnabled(False)  # Только просмотр
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
    
    def load_table(self, table_name):
        """Загрузка данных выбранной таблицы в TableWidget"""
        self.current_table = table_name
        conn = sqlite3.connect('linda.sqlite')
        cursor = conn.cursor()
        
        # В зависимости от выбранной таблицы выполняем соответствующий запрос
        if table_name == "Продукты":
            cursor.execute("SELECT * FROM Products")
            data = cursor.fetchall()
            headers = ["ID", "Название", "Тип", "Страна", "Кол-во", "Материал", "Обивка", "Цена"]
        elif table_name == "Клиенты":
            cursor.execute("SELECT * FROM Clients")
            data = cursor.fetchall()
            headers = ["ID", "Фамилия", "Имя", "Отчество", "Адрес", "Город"]
        else:  # Заказы - делаем JOIN для отображения имен вместо ID
            cursor.execute("""
                SELECT o.order_id, c.last_name, p.name, o.order_date, o.order_number 
                FROM Orders o 
                JOIN Clients c ON o.client_id=c.client_id 
                JOIN Products p ON o.product_id=p.product_id
            """)
            data = cursor.fetchall()
            headers = ["ID", "Клиент", "Товар", "Дата", "Номер"]
        
        conn.close()
        
        # Настраиваем таблицу и заполняем данными
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget.setRowCount(len(data))
        
        for row, row_data in enumerate(data):
            for col, val in enumerate(row_data):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(val)))
        
        self.ui.tableWidget.hideColumn(0)  # Скрываем столбец с ID
        self.ui.tableWidget.resizeColumnsToContents()  # Подгоняем ширину столбцов
    
    def get_selected_id(self):
        """Получить ID выбранной записи (первый столбец таблицы)"""
        row = self.ui.tableWidget.currentRow()
        if row == -1:
            return None
        return self.ui.tableWidget.item(row, 0).text()
    
    def add_record(self):
        """Добавление новой записи в выбранную таблицу"""
        if self.current_table == "Продукты":
            dlg = ProductDialog(self)
            if dlg.exec_() == QDialog.Accepted:
                data = dlg.get_data()
                conn = sqlite3.connect('linda.sqlite')
                conn.execute("INSERT INTO Products (name, type, country, items_count, material, upholstery, price) VALUES (?,?,?,?,?,?,?)", data)
                conn.commit()
                conn.close()
                self.load_table(self.current_table)
                QMessageBox.information(self, "Успех", "Товар добавлен")
        elif self.current_table == "Клиенты":
            dlg = ClientDialog(self)
            if dlg.exec_() == QDialog.Accepted:
                data = dlg.get_data()
                conn = sqlite3.connect('linda.sqlite')
                conn.execute("INSERT INTO Clients (last_name, first_name, middle_name, address, city) VALUES (?,?,?,?,?)", data)
                conn.commit()
                conn.close()
                self.load_table(self.current_table)
                QMessageBox.information(self, "Успех", "Клиент добавлен")
        else:  # Заказы
            dlg = OrderDialog(self)
            if dlg.exec_() == QDialog.Accepted:
                data = dlg.get_data()
                conn = sqlite3.connect('linda.sqlite')
                try:
                    conn.execute("INSERT INTO Orders (client_id, product_id, order_date, order_number) VALUES (?,?,?,?)", data)
                    conn.commit()
                    self.load_table(self.current_table)
                    QMessageBox.information(self, "Успех", "Заказ добавлен")
                except:
                    QMessageBox.critical(self, "Ошибка", "Номер заказа уже существует")
                conn.close()
    
    def edit_record(self):
        """Редактирование выбранной записи"""
        id_val = self.get_selected_id()
        if not id_val:
            QMessageBox.critical(self, "Ошибка", "Выберите запись")
            return
        
        conn = sqlite3.connect('linda.sqlite')
        cursor = conn.cursor()
        
        if self.current_table == "Продукты":
            cursor.execute("SELECT * FROM Products WHERE product_id=?", (id_val,))
            record = cursor.fetchone()
            conn.close()
            dlg = ProductDialog(self, record)
            if dlg.exec_() == QDialog.Accepted:
                data = dlg.get_data()
                conn = sqlite3.connect('linda.sqlite')
                conn.execute("UPDATE Products SET name=?, type=?, country=?, items_count=?, material=?, upholstery=?, price=? WHERE product_id=?", data + (id_val,))
                conn.commit()
                conn.close()
                self.load_table(self.current_table)
                QMessageBox.information(self, "Успех", "Товар обновлен")
        elif self.current_table == "Клиенты":
            cursor.execute("SELECT * FROM Clients WHERE client_id=?", (id_val,))
            record = cursor.fetchone()
            conn.close()
            dlg = ClientDialog(self, record)
            if dlg.exec_() == QDialog.Accepted:
                data = dlg.get_data()
                conn = sqlite3.connect('linda.sqlite')
                conn.execute("UPDATE Clients SET last_name=?, first_name=?, middle_name=?, address=?, city=? WHERE client_id=?", data + (id_val,))
                conn.commit()
                conn.close()
                self.load_table(self.current_table)
                QMessageBox.information(self, "Успех", "Клиент обновлен")
        else:  # Заказы
            cursor.execute("SELECT * FROM Orders WHERE order_id=?", (id_val,))
            record = cursor.fetchone()
            conn.close()
            dlg = OrderDialog(self, record)
            if dlg.exec_() == QDialog.Accepted:
                data = dlg.get_data()
                conn = sqlite3.connect('linda.sqlite')
                try:
                    conn.execute("UPDATE Orders SET client_id=?, product_id=?, order_date=?, order_number=? WHERE order_id=?", data + (id_val,))
                    conn.commit()
                    self.load_table(self.current_table)
                    QMessageBox.information(self, "Успех", "Заказ обновлен")
                except:
                    QMessageBox.critical(self, "Ошибка", "Номер заказа уже существует")
                conn.close()
    
    def delete_record(self):
        """Удаление выбранной записи"""
        id_val = self.get_selected_id()
        if not id_val:
            QMessageBox.critical(self, "Ошибка", "Выберите запись")
            return
        
        # Подтверждение удаления
        if QMessageBox.question(self, "Подтверждение", "Удалить запись?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
            return
        
        conn = sqlite3.connect('linda.sqlite')
        if self.current_table == "Продукты":
            conn.execute("DELETE FROM Products WHERE product_id=?", (id_val,))
        elif self.current_table == "Клиенты":
            conn.execute("DELETE FROM Clients WHERE client_id=?", (id_val,))
        else:
            conn.execute("DELETE FROM Orders WHERE order_id=?", (id_val,))
        conn.commit()
        conn.close()
        self.load_table(self.current_table)
        QMessageBox.information(self, "Успех", "Запись удалена")
    
    def show_about(self):
        """Показать информацию об авторе"""
        QMessageBox.about(self, "Об авторе", 
                          "Разработчик: Маличева Валерия\n"
                          "Группа: 432\n"
                          "Мебельный магазин 'ЛИНДА'\n")
    
    def show_guide(self):
        """Показать руководство пользователя"""
        guide_text = (
            "РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ\n\n"
            "1. АВТОРИЗАЦИЯ:\n"
            "admin / admin - вход как Администратор (полный доступ)\n"
            "manager / manager - вход как Менеджер (только просмотр и добавление)\n"
            "любой другой логин - вход как Гость (только просмотр)\n\n"
            "2. РАБОТА С ДАННЫМИ:\n"
            "Выберите таблицу из выпадающего списка в правом верхнем углу\n"
            "Доступны таблицы: Продукты, Клиенты, Заказы\n\n"
            "3. ДОБАВЛЕНИЕ ЗАПИСИ:\n"
            "Нажмите кнопку 'Добавить запись'\n"
            "Заполните все поля в открывшемся окне\n"
            "4. РЕДАКТИРОВАНИЕ ЗАПИСИ:\n"
            "   - Выберите строку в таблице (нажмите на нее)\n"
            "   - Нажмите кнопку 'Редактировать запись'\n"
            "5. УДАЛЕНИЕ ЗАПИСИ:\n"
            "   - Выберите строку в таблице\n"
            "   - Нажмите кнопку 'Удалить запись'\n"
            "   - Подтвердите удаление\n\n"
            "6. ПРАВА ДОСТУПА:\n"
            "   - Администратор: добавление, редактирование, удаление\n"
            "   - Менеджер: только просмотр и добавление\n"
            "   - Гость: только просмотр\n\n"
        )
        QMessageBox.information(self, "Руководство пользователя", guide_text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  
    create_db()                         
    main_win = MainWindow()                 
    login_win = LoginWindow()               
    login_win.show()                         
    sys.exit(app.exec_())               

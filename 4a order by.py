 import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем и сортируем пользователей по возрасту по убыванию
cursor.execute('SELECT username, age FROM Users ORDER BY age DESC')
results = cursor.fetchall()

for row in results:
    print(row)

# Закрываем соединение
connection.close()

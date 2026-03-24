import sqlite3
# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my database.db')
cursor = connection.cursor()
# Выбираем первого пользователя
cursor.execute ('SELECT * FROM Users')
first user = cursor.fetchone()
print (first user)
# Выбираем первых 5 пользователей
cursor.execute('SELECT * FROM Users')
first five users = cursor.fetchmany(5)
print (first five users)
# Выбираем всех пользователей
cursor.execute ('SELECT * FROM Users')
all users = cursor.fetchall()
print (all users)
# Закрываем соединение
connection.close ()

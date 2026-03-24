import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Подсчет общего числа пользователей
cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()

# Вывод результата
print(f'Общее количество пользователей: {total_users}')

# Закрытие соединения
connection.close()

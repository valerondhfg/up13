import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Запрос для получения имен и возраста пользователей старше 25 лет
cursor.execute('SELECT username, age FROM Users WHERE age > ?', (25,))

# Получение результатов запроса
results = cursor.fetchall()

# Вывод результатов
for row in results:
    print(row)

# Закрытие соединения с базой данных
connection.close()

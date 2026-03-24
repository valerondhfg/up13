import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем и сортируем пользователей по возрасту по убыванию
cursor.execute("""
    SELECT username, age, AVG(age)
    FROM Users
    GROUP BY age
    HAVING AVG(age) > ?
    ORDER BY age DESC
""", (30,))

# Получаем результаты
results = cursor.fetchall()

# Выводим результаты
for row in results:
    print(row)

# Закрываем соединение
connection.close()

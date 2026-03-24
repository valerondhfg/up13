#count
import sqlite3#Подключение к базе данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Подсчет общего числа пользователей
cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()

# Вывод результата
print(f'Общее количество пользователей: {total_users}')

# Закрытие соединения
connection.close()

#sum
import sqlite3
connection = sqlite3.connect('my database.db')
cursor = connection.cursor ()
# Вычисление суммы возрастов пользователей
cursor.execute('SELECT SUM(age) FROM Users') total age = cursor.fetchone() [0]
print ('Общая сумма возрастов пользователей:', total age)
connection.close ()

#avg
import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Вычисление среднего возраста пользователей
cursor.execute('SELECT AVG(age) FROM Users')
average_age = cursor.fetchone()

# Проверка на NULL
if average_age is None:
    print("Средний возраст пользователей не определён.")
else:
    print(f"Средний возраст пользователей: {average_age}")

# Закрытие соединения
connection.close()

#min
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Нахождение минимального возраста
cursor.execute('SELECT MIN(age) FROM Users')
min_age = cursor.fetchone()

print('Минимальный возраст среди пользователей:', min_age)

connection.close()


#max
import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Нахождение максимального возраста
cursor.execute('SELECT MAX(age) FROM Users')
max_age = cursor.fetchone()

# Вывод результата
print('Максимальный возраст среди пользователей:', max_age)

# Закрытие соединения
connection.close()


import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем подготовленный запрос
query = 'SELECT * FROM Users WHERE age > ?'
cursor.execute(query, (25,))

# Выводим результаты
users = cursor.fetchall()
for user in users:
    print(user)

# Закрываем соединение
connection.close()


   #2
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем представление для активных пользователей
cursor.execute('''
    CREATE VIEW ActiveUsers AS 
    SELECT * FROM Users 
    WHERE is_active = 1
''')

# Выбираем активных пользователей
cursor.execute('SELECT * FROM ActiveUsers')
active_users = cursor.fetchall()

# Выводим результаты
for user in active_users:
    print(user)

# Закрываем соединение
connection.close()


#3
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Создаем триггер для обновления времени создания при вставке новой записи
cursor.execute("""
CREATE TRIGGER IF NOT EXISTS update_created_at
    AFTER INSERT ON Users
    BEGIN
        UPDATE Users SET created_at = CURRENT_TIMESTAMP
        WHERE id = NEW.id;
    END;
""")

# Сохраняем изменения
connection.commit()

# Закрываем соединение
connection.close()




#4
import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем индекс для столбца "username"
cursor.execute('CREATE INDEX idx_username ON Users (username)')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()

import sqlite3 as sl
from easygui import *

def select_all():
    cur.execute("SELECT * FROM users;")
    return cur.fetchall()

def add_values():
    cur.execute("INSERT INTO users VALUES (1,'Ваня','Петров');")
    cur.execute("INSERT INTO users VALUES (2,'Сергей','Сергеев');")

def add_contact(name):
    phones = enterbox(f"Введите телефоны для {name} (через запятую):")
    email = enterbox(f"Введите email для {name}:")
    birthday = enterbox(f"Введите дату рождения для {name} (в формате DD.MM.YYYY):")
    company = enterbox(f"Введите компанию для {name}:")

    # Извлекаем только цифры из строки с телефоном
    phone_numbers = [int(''.join(filter(str.isdigit, phone))) for phone in phones.split(',')]

    phonebook[name] = {'phones': phone_numbers if phone_numbers else [],
                       'email': email if email else '',
                       'birthday': birthday if birthday else '',
                       'company': company if company else ''}
    msgbox(f"Контакт {name} успешно добавлен.", "Добавление контакта")

# Инициализация phonebook
phonebook = {}

conn = sl.connect("test_evening.db")
cur = conn.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS users
            (
            id INTEGER PRIMARY KEY,
            name TEXT,
            surname TEXT
            );
            """)

choice = choicebox("Выберите запрос", "Главная форма", 
                   ['Все записи', 'Добавить контакт', 'Просмотреть все контакты', 'Изменить контакт', 'Удалить контакт'])

if choice == "Все записи":
    msg = str(select_all())
    msgbox(msg, "Результат запроса")
elif choice == "Добавить контакт":
    name_to_add = enterbox("Введите имя для добавления контакта:")
    add_contact(name_to_add)
elif choice == "Просмотреть все контакты":
    all_contacts = ""
    for name, contact_info in phonebook.items():
        all_contacts += f"Имя: {name}\nТелефоны: {', '.join(map(str, contact_info['phones']))}\nEmail: {contact_info['email']}\nДень рождения: {contact_info['birthday']}\nКомпания: {contact_info['company']}\n\n"
    msgbox(all_contacts, "Все контакты")

conn.commit()
conn.close()
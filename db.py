import sqlite3
from sqlite3 import Error
import csv

Q_GETDICT = 'SELECT persons.second_name, persons.first_name, persons.patronymic, directory.phone FROM directory INNER JOIN persons ON directory.person_id = persons.id'

connection = None
cursor = None


def create_connection(path):
    global connection
    try:
        connection = sqlite3.connect(path)
        print("Подключение к базе данных SQLite прошло успешно")
    except Error as e:
        print(f"Произошла ошибка '{e}'")
    connection.text_factory = lambda s: str(s, 'utf-8')
    return connection


def get_cursor():
    global cursor, connection
    cursor = connection.cursor()


def get_entries(number: int):
    cursor.execute(Q_GETDICT)
    result = cursor.fetchmany(number)
    return result

def find_entrie(fcs: str, create_on_fail:bool = True):
    global cursor
    buffer = [x.strip(' ') for x in fcs.split()]
    d = {'fn': buffer[0], 'sn': buffer[1], 'p': buffer[2]}
    test = cursor.execute(Q_GETDICT + ' WHERE persons.second_name =:sn AND persons.first_name =:fn AND persons.patronymic =:p', d)

def create_entrie():
    pass

def db_import(file: str, format: str = 'csv'):
    global cursor
    if format in ['csv', 'txt']:
        with open(file, 'r', encoding="utf-8") as fin:
            dr = csv.DictReader(fin)
            for i in dr:
                buffer = (i['second_name'], i['first_name'],
                        i['patronymic'], i['phone'])
                cursor.execute(
                    "INSERT INTO persons (second_name, first_name, patronymic) VALUES (?, ?, ?);", buffer[:-1])
                cursor.execute("INSERT INTO directory (person_id, phone) VALUES (?, ?);", (int(
                    cursor.lastrowid), buffer[-1]))
                connection.commit()


def db_export(file: str, format: str = 'csv'):
    global cursor
    if format in ['csv', 'txt']:
        data = cursor.execute(Q_GETDICT)
        with open(file, 'w', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ['second_name', 'first_name', 'patronymic', 'phone'])
            writer.writerows(data)

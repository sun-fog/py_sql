import psycopg2

def create_db(conn):
# Функция, создающая структуру БД (таблицы)

    with conn.cursor() as cur:
        # создание таблицы клиентов
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client (
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(80) NOT NULL, 
            last_name VARCHAR(80) NOT NULL,
            email VARCHAR(80) NOT NULL,
            phones TEXT [] 
        );
        """)

        conn.commit()  # фиксируем в БД

def add_client(conn, first_name, last_name, email, phones):
# Функция, позволяющая добавить нового клиента

    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(first_name, last_name, email, phones) VALUES(%s, %s, %s, %s);
        """, (first_name, last_name, email, phones))
        conn.commit()  # фиксируем в БД

def add_phone(conn, client_id, phone):
# Функция, позволяющая добавить телефон для существующего клиента

    with conn.cursor() as cur:
        cur.execute("""    
        UPDATE client
        SET phones = array_append(phones, %s)
        WHERE client_id = %s; 
        """, (phone, client_id))
        conn.commit()  # фиксируем в БД

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
# Функция, позволяющая изменить данные о клиенте

    with conn.cursor() as cur:
        cur.execute("""    
        UPDATE client
        SET first_name = %s
        WHERE client_id = %s;
    
        UPDATE client
        SET last_name = %s
        WHERE client_id = %s;
    
        UPDATE client
        SET email = %s
        WHERE client_id = %s;
    
        UPDATE client
        SET phones = %s
        WHERE client_id = %s;    
         
        """, (first_name, client_id, last_name, client_id, email, client_id, phones, client_id))
        conn.commit()  # фиксируем в БД

def delete_phone(conn, client_id, phone):
# Функция, позволяющая удалить телефон для существующего клиента

    with conn.cursor() as cur:
        cur.execute("""    
        UPDATE client
        SET phones = array_remove(phones, %s)
        WHERE client_id = %s; 
        """, (phone, client_id))
        conn.commit()  # фиксируем в БД

def delete_client(conn, client_id):
# Функция, позволяющая удалить существующего клиента

    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client WHERE client_id=%s;
        """, (client_id,))

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону

    with conn.cursor() as cur:
        # поиск клиента по телефону
        cur.execute("""
        SELECT client_id, first_name, last_name, email, phones FROM client WHERE first_name = %s 
        OR last_name = %s
        OR email = %s
        OR %s = ANY (phones);
        """, (first_name, last_name, email, phone))
        return cur.fetchone()

with psycopg2.connect(database="clients_db", user="postgres", password="MaxPlant1!", host="localhost", port="5432") as conn:
	
    create_db(conn)
    add_client(conn, 'Иван', 'Петров', 'ivan_petrov@mail.ru', '{"+7-911-111-11-11", "+7-921-111-11-11"}')
    add_client(conn, 'Пётр', 'Иванов', 'petr_ivanov@mail.ru', '{"+7-911-222-22-22", "+7-921-222-22-22"}')
    add_client(conn, 'Алексей', 'Летучий', 'alex_letuchy@mail.ru', '{"+7-911-333-33-33"}')    
    add_phone(conn, 3, '+7-921-333-33-33')
    change_client(conn, 1, first_name='Иван', last_name='Петров', email='ivan_petrov@yandex.ru', phones='{"+7-911-111-11-11", "+7-921-111-11-11"}')
    delete_phone(conn, 1, '+7-911-111-11-11')
    delete_client(conn, 2)
    person = find_client(conn, first_name='Иван')
    print('Найден клиент', person)

conn.close()

import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="12345678",
        database="afisha",
        port=5432
    )

except (Exception, Error) as error:
    print("Ошибка при подключении к базе данных", error)


def get_category():
    with connection.cursor() as cursor:
        cursor.execute("select * from categories")
        data = cursor.fetchall()
    return data


def set_user(user_id: int, nickname: str, username: str, category_ids: list) -> bool:
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                'insert into "users" (tg_user_id, nickname, username, category_ids) values (%s, %s, %s, %s) ON CONFLICT (tg_user_id) DO NOTHING RETURNING *',
                (user_id, nickname, username, category_ids)
            )
            data = cursor.fetchone()
            connection.commit()
            return True if data else False

        except Error as e:
            print(e)

            if e.pgcode == "23505":
                return False


def update_category_ids(user_id: int, category_ids: list) -> None:
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                'update "users" set category_ids = %s where tg_user_id = %s',
                (category_ids, user_id)
            )
            connection.commit()
        except Error:
                pass


def get_user_category(user_id: int) -> list:
    with connection.cursor() as cursor:
        try:
            cursor.execute('select category_ids from "users" where tg_user_id = %s', (user_id,))
            data = cursor.fetchone()[0]

            res = []

            for i in data:
                cursor.execute('select name from categories where id = %s', (i,))
                try:
                    res.append(cursor.fetchone()[0])
                except TypeError:
                    pass
            return res
        except Error as e:
            print(e)


def get_last_mailings(categories: list) -> list:
    data = []

    with connection.cursor() as cursor:
        try:
            for i in categories:
                cursor.execute('select * from mailings where categories @> %s', ([i],))
                try:
                    data.append(*cursor.fetchall())
                except TypeError:
                    pass

            return data
        except Error as e:
            print(e)

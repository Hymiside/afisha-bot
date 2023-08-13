import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="putinbest",
        database="afisha",
        port=5432
    )
    cursor = connection.cursor()

except (Exception, Error) as error:
    print("Ошибка при подключении к базе данных", error)


def get_category():
    cursor.execute("select * from category")
    data = cursor.fetchall()
    return data


def set_user(user_id: int, nickname: str, username: str, category_ids: list) -> bool:
    try:
        cursor.execute(
            'insert into "user" (tg_user_id, nickname, username, category_ids) values (%s, %s, %s, %s)',
            (user_id, nickname, username, category_ids)
        )
        connection.commit()
        return True

    except Error as e:
        if e.pgcode == "23505":
            return False


def update_category_ids(user_id: int, category_ids: list) -> None:
    try:
        cursor.execute(
            'update "user" set category_ids = %s where tg_user_id = %s',
            (category_ids, user_id)
        )
        connection.commit()
    except Error:
            pass


def get_user_category(user_id: int) -> list:
    try:
        cursor.execute('select category_ids from "user" where tg_user_id = %s', (user_id,))
        data = cursor.fetchone()[0]

        res = []

        for i in data:
            cursor.execute('select category from category where id = %s', (i,))
            res.append(cursor.fetchone()[0])

        return res
    except Error as e:
        print(e)
# wishlist.py
import pymysql
import random
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, userid


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


def get_wishlist(userid):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            query = ("SELECT w.*, b.ISBN, title, authors, publisher, "
                     "DATE_FORMAT(yop,'%Y-%m-%d') AS yop, "
                     "available_copies, price, format, keywords, subject, image_loc "
                     "FROM wishlist AS w LEFT JOIN books AS b "
                     "ON b.ISBN = w.isbn WHERE user_id = %s")
            cursor.execute(query, (userid,))
            result = cursor.fetchall()

            for item in result:
                q = "SELECT * FROM rating WHERE isbn = %s"
                cursor.execute(q, (item.get('isbn'),))
                item['rating'] = cursor.fetchall()

        connection.commit()
        return result
    except Exception as e:
        print(e, 'in get_wishlist')
        return []
    finally:
        connection.close()


def add_to_wishlist(isbn, userid):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            get_query = "SELECT * FROM wishlist WHERE user_id = %s"
            cursor.execute(get_query, (userid,))
            get_result = cursor.fetchall()

            wishlist_id = str(random.randint(0, 9999999))
            user_query = "SELECT * FROM customer WHERE Login_id = %s"
            cursor.execute(user_query, (userid,))
            user_data = cursor.fetchall()

            if not user_data:
                raise Exception("User not found")

            wish_list_name = user_data[0].get('Name').split(' ')[0] + "'s wishlist"

            if get_result:
                wishlist_id = get_result[0].get('wishlist_id')

            query = ("INSERT INTO wishlist (user_id, wishlist_id, isbn, name) "
                     "VALUES (%s, %s, %s, %s)")
            cursor.execute(query, (userid, wishlist_id, isbn, wish_list_name))

        connection.commit()
    except Exception as e:
        print(e, 'in add_to_wishlist')
    finally:
        connection.close()


def remove_from_wishlist(wishlist_id, userid):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            query = "DELETE FROM wishlist WHERE id = %s AND user_id = %s"
            cursor.execute(query, (wishlist_id, userid))

        connection.commit()
    except Exception as e:
        print(e, 'in remove_from_wishlist')
    finally:
        connection.close()


def update_wishlist(wishlist_id=None, isbn=None, operation_type='add'):
    try:
        if operation_type == 'add':
            add_to_wishlist(isbn, userid)
        else:
            remove_from_wishlist(wishlist_id, userid)
    except Exception as e:
        print(e, 'in update_wishlist')

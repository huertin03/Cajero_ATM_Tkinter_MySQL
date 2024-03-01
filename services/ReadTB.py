import mysql.connector


def read_tb(nombretb, conn):
    sql_select = f"SELECT * FROM {nombretb}"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_select)
        return cursor.fetchall()
    except mysql.connector.Error as error:
        print("Error al leer tabla en MySQL: {}".format(error))
    return []

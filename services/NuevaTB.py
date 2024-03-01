import mysql.connector


def crear_tb(nombretb, conn):
    mysql_create = f"CREATE TABLE {nombretb}(MONEDA DECIMAL(10,2), CANTIDAD INT UNSIGNED NOT NULL CHECK (CANTIDAD >= 0))"
    try:
        cursor = conn.cursor()
        cursor.execute(mysql_create)
    except mysql.connector.Error as error:
        print("Error al crear nueva tabla en MySQL: {}".format(error))
    finally:
        rellenar_tb(nombretb, conn)


def rellenar_tb(nombretb, conn):
    sql_insert = f"INSERT INTO {nombretb} (MONEDA, CANTIDAD) VALUES (%s,%s);"
    try:
        cursor = conn.cursor()
        for exponente in range(2, -3, -1):
            for multiplicador in [5, 2, 1]:
                moneda = multiplicador * (10 ** exponente)
                cantidad = 10
                cursor.execute(sql_insert, (moneda, cantidad))
        conn.commit()
    except mysql.connector.Error as error:
        print("Error al rellenar tabla en MySQL: {}".format(error))

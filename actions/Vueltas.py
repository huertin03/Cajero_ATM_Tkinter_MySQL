import mysql.connector
from decimal import Decimal


class Vueltas:
    def __init__(self, conn, banco):
        self.conn = conn
        self.banco = banco
        self.SQL_UPDATE = f"UPDATE {self.banco} SET CANTIDAD = %s WHERE MONEDA = %s"
        self.SQL_SELECT = f"SELECT CANTIDAD FROM {self.banco} WHERE MONEDA = %s"

    def get_cantidad(self, moneda):
        cantidad = 0
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.SQL_SELECT, (moneda,))
            result = cursor.fetchone()
            if result:
                cantidad = result[0]

            cursor.close()
        except mysql.connector.Error as error:
            print("Error de MySQL:", error)
        except Exception as e:
            print("Error:", e)

        return cantidad

    def llenar_tb(self, pago):
        moneda_cantidad = {}
        pago_separado = pago.split("#")

        for pago_individual in pago_separado:
            pago_cantidad = pago_individual.split("-")
            moneda = float(pago_cantidad[1])
            cantidad = int(pago_cantidad[0])

            if moneda in moneda_cantidad:
                moneda_cantidad[moneda] += cantidad
            else:
                moneda_cantidad[moneda] = cantidad

        try:
            cursor = self.conn.cursor()
            for moneda, cantidad in moneda_cantidad.items():
                antigua_cantidad = self.get_cantidad(moneda)
                nueva_cantidad = antigua_cantidad + cantidad
                cursor.execute(self.SQL_UPDATE, (nueva_cantidad, moneda))

            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as error:
            print("Error de MySQL:", error)
        except Exception as e:
            print("Error:", e)

    def devolver_vueltas(self, vueltas):
        try:
            self.conn.autocommit = False
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {self.banco}")
            result_set = cursor.fetchall()
            self.conn.commit()

            for row in result_set:
                moneda = Decimal(row[0])
                cantidad = row[1]
                while int(moneda * 100) <= int(vueltas * 100) and cantidad > 0:
                    cantidad -= 1
                    vueltas = Decimal(int(vueltas * 100) - int(moneda * 100)) / 100
                    cursor.execute(self.SQL_UPDATE, (cantidad, moneda))

                if vueltas <= 0:
                    self.conn.commit()
                    return True
            self.conn.rollback()
            return False

        except mysql.connector.Error as error:
            print("Error de MySQL:", error)
            return False
        except Exception as e:
            print("Error:", e)
            return False

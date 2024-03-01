def update_cantidad(moneda, cantidad, banco, conn):
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {banco} SET cantidad = {cantidad} WHERE moneda = '{moneda}'")
    conn.commit()
    cursor.close()

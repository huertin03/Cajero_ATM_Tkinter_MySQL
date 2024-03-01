def evaluar_importe(importe):
    try:
        float(importe)
    except ValueError:
        return False

    if len(importe.split(".")) > 1 and len(importe.split(".")[1]) > 2:
        return False

    return True


def evaluar_pago(pago):
    pago_separado = pago.split("#")
    try:
        for pago_individual in pago_separado:
            moneda_valida = False
            pago_cantidad = pago_individual.split("-")
            if len(pago_cantidad) > 2:
                return False
            for cantidad in pago_cantidad:
                float(cantidad)
            for t in range(2, -3, -1):
                for m in [5, 2, 1]:
                    if float(pago_cantidad[1]) == (m * 10 ** t):
                        moneda_valida = True
                        break
                if moneda_valida:
                    break
            if not moneda_valida:
                return False
        return True
    except ValueError as e:
        return False


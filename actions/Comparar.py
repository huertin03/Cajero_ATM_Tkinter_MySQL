def comparar_pago(pago, importe):
    vueltas = 0
    float_pago = 0
    pago_separado = pago.split("#")
    for pago_individual in pago_separado:
        pago_cantidad = pago_individual.split("-")
        float_pago += float(pago_cantidad[0]) * float(pago_cantidad[1])
    vueltas = float_pago - importe
    return vueltas

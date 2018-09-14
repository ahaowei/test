import decimal


def round_decimal(x, digits = 0):
    x = decimal.Decimal(str(x))
    if digits == 0:
        return int(x.quantize(decimal.Decimal("1"), rounding='ROUND_HALF_UP'))
    if digits > 1:
        string = '1e' + str(-1*digits)
    else:
        string = '1e' + str(-1*digits)
    return float(x.quantize(decimal.Decimal(string), rounding='ROUND_HALF_UP'))

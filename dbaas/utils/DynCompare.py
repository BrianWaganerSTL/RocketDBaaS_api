def DynCompare(left, operator, right):
    lValue = float(left)
    rValue = float(right)

    print(str(lValue) + operator + str(rValue))

    if (operator == '<'):
        return lValue < rValue;
    elif (operator == '<='):
        return lValue <= rValue;
    elif (operator == '>'):
        return lValue > rValue;
    elif (operator == '>='):
        return lValue >= rValue;
    elif (operator == '=='):
        return lValue == rValue;
    elif (operator == '!='):
        return lValue != rValue;
    else:
        return False;

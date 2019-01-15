def DynCompare(left, operator, right):
    leftValue = float(left)
    rightValue = float(right)

    if (operator == '<'):
        return leftValue < rightValue;
    elif (operator == '<='):
        return leftValue <= rightValue;
    elif (operator == '>'):
        return leftValue > rightValue;
    elif (operator == '>='):
        return leftValue >= rightValue;
    elif (operator == '=='):
        return leftValue == rightValue;
    elif (operator == '!='):
        return leftValue != rightValue;
    else:
        return False;

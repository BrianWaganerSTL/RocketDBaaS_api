from monitor.models import PredicateTypeChoices


def DynCompare(left, operator, right):
    leftValue = float(left)
    rightValue = float(right)

    if (operator == PredicateTypeChoices.LTH):
        return leftValue < rightValue
    elif (operator == PredicateTypeChoices.LTE):
        return leftValue <= rightValue
    elif (operator == PredicateTypeChoices.GTH):
        return leftValue > rightValue
    elif (operator == PredicateTypeChoices.GTE):
        return leftValue >= rightValue
    elif (operator == PredicateTypeChoices.EQ):
        return leftValue == rightValue
    elif (operator == PredicateTypeChoices.NE):
        return leftValue != rightValue
    else:
        return False

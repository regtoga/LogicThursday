import utilsV1 as utils

def NOT_GATE(X1: bool) -> bool:
    """accept one bool and does the NOT calculation on it.\n
        Truth Table:\n
        *--------------*\n
        |INPUT1|OUTPUT1|\n
        |   0  |   1   |\n
        |   1  |   0   |\n
        *--------------*\n"""
    #print(f"NOT of {X1} = {int(not(X1))}")
    NOT = (int(not(X1)))
    return NOT

def AND_GATE(X1: bool, X2: bool) -> bool:
    """accept two bools and does the AND calculation on them.\n
        Truth Table:\n
        *---------------------*\n
        |INPUT1|INPUT2|OUTPUT1|\n
        |   0  |   0  |   0   |\n
        |   0  |   1  |   0   |\n
        |   1  |   0  |   0   |\n
        |   1  |   1  |   1   |\n
        *---------------------*\n
    """
    #print(f"AND of {X1}, {X2} = {X1 and X2}")
    AND = ((X1 and X2))
    return AND

def OR_GATE(X1: bool, X2: bool) -> bool:
    """accept two bools and does the OR calculation on them.\n
        Truth Table:\n
        *---------------------*\n
        |INPUT1|INPUT2|OUTPUT1|\n
        |   0  |   0  |   0   |\n
        |   0  |   1  |   1   |\n
        |   1  |   0  |   1   |\n
        |   1  |   1  |   1   |\n
        *---------------------*\n
    """
    #print(f"OR of {X1}, {X2} = {X1 or X2}")
    OR = ((X1 or X2))
    return OR



#harder gates
def NAND_GATE(X1: bool, X2: bool) -> bool:
    """accept two bools and does the NAND calculation on them.\n
        Truth Table:\n
        *---------------------*\n
        |INPUT1|INPUT2|OUTPUT1|\n
        |   0  |   0  |   1   |\n
        |   0  |   1  |   1   |\n
        |   1  |   0  |   1   |\n
        |   1  |   1  |   0   |\n
        *---------------------*\n
    """
    #print(NOT_GATE(AND_GATE(X1, X2)))
    NAND = NOT_GATE(AND_GATE(X1, X2))
    return NAND

def XOR_GATE(X1: bool, X2: bool) -> bool:
    """accept two bools and does the NAND calculation on them.\n
        Truth Table:\n
        *---------------------*\n
        |INPUT1|INPUT2|OUTPUT1|\n
        |   0  |   0  |   1   |\n
        |   0  |   1  |   0   |\n
        |   1  |   0  |   0   |\n
        |   1  |   1  |   1   |\n
        *---------------------*\n
    """
    XOR = AND_GATE(OR_GATE(X1, X2), NAND_GATE(X1, X2))
    return XOR



#not really a gate!

#ADDERS
def ADDER(X1: bool, X2: bool, CarryIn: bool) -> bool:
    """Takes input(x, y, z) as in x1 + y1 carry in z"""
    SUM = XOR_GATE(XOR_GATE(X1, X2), CarryIn)
    CARRYOUT = OR_GATE(AND_GATE(XOR_GATE(X1, X2), CarryIn), AND_GATE(X2, X1))

    return SUM, CARRYOUT

def TWOBITADDER(XBools: list, YBools: list, CarryIn: bool) -> bool:
    """Takes input(xx, yy, z) as in x1 + y1 carry in z"""
    X2, X1 = utils.twoBitList_into_individual_bools(XBools)
    Y2, Y1 = utils.twoBitList_into_individual_bools(YBools)

    xout1, adder1out = ADDER(X1, Y1, CarryIn)
    xout2, carryout = ADDER(X2, Y2, adder1out)

    output = utils.twoIndividualBools_into_twoBitList(xout2, xout1)
    return output, carryout

def FOURBITADDER(XBools: list, YBools: list, CarryIn: bool) -> bool:
    """Takes input(xxxx, yyyy, z) as in x1 + y1 carry in z\n
    Two Outputs, -> output: list, carryout: bool
    """
    X4, X3, X2, X1 = utils.fourBitList_into_individual_bools(XBools)
    Y4, Y3, Y2, Y1 = utils.fourBitList_into_individual_bools(YBools)

    xout1, adder1out = ADDER(X1, Y1, CarryIn)
    xout2, adder2out = ADDER(X2, Y2, adder1out)
    xout3, adder3out = ADDER(X3, Y3, adder2out)
    xout4, carryout = ADDER(X4, Y4, adder3out)

    output = utils.fourIndividualBools_into_fourBitList(xout4, xout3, xout2, xout1)

    return output, carryout

def EIGHTBITADDER(XBools: list, YBools: list, CarryIn: bool) -> bool: 
    """Takes input(xxxxxxxx, yyyyyyyy, z) as in x1 + y1 carry in z"""
    X8, X7, X6, X5, X4, X3, X2, X1 = utils.eightBitList_into_individual_bools(XBools)
    Y8, Y7, Y6, Y5, Y4, Y3, Y2, Y1 = utils.eightBitList_into_individual_bools(YBools)

    xout1, adder1out = ADDER(X1, Y1, CarryIn)
    xout2, adder2out = ADDER(X2, Y2, adder1out)
    xout3, adder3out = ADDER(X3, Y3, adder2out)
    xout4, adder4out = ADDER(X4, Y4, adder3out)
    xout5, adder5out = ADDER(X5, Y5, adder4out)
    xout6, adder6out = ADDER(X6, Y6, adder5out)
    xout7, adder7out = ADDER(X7, Y7, adder6out)
    xout8, carryout = ADDER(X8, Y8, adder7out)

    output = utils.eightIndividualBools_into_eightBitList(xout8, xout7, xout6, xout5, xout4, xout3, xout2, xout1)

    return output, carryout

def TWOBITADDERsmall(XBools: list, YBools: list, CarryIn: bool) -> bool:
    """Takes input(xx, yy, z) as in x1 + y1 carry in z"""
    X2, X1 = utils.twoBitList_into_individual_bools(XBools)
    Y2, Y1 = utils.twoBitList_into_individual_bools(YBools)

    xout1, adder1out = ADDER(X1, Y1, CarryIn)
    xout2, carryout = ADDER(X2, Y2, adder1out)

    output = utils.twoIndividualBools_into_twoBitList(xout2, xout1)
    return output, carryout

def FOURBITADDERsmall(XBools: list, YBools: list, CarryIn: bool) -> bool:
    """Takes input(xxxx, yyyy, z) as in x1 + y1 carry in z"""
    X4, X3, X2, X1 = utils.fourBitList_into_individual_bools(XBools)
    Y4, Y3, Y2, Y1 = utils.fourBitList_into_individual_bools(YBools)

    xout1, adder1out = TWOBITADDERsmall([X2,X1], [Y2,Y1], CarryIn)
    xout2, carryout = TWOBITADDERsmall([X4,X3], [Y4,Y3], adder1out)

    out2, out1 = utils.twoBitList_into_individual_bools(xout1)
    out4, out3 = utils.twoBitList_into_individual_bools(xout2)
    output = utils.fourIndividualBools_into_fourBitList(out4, out3, out2, out1)
    return output, carryout


def EIGHTBITADDERsmall(XBools: list, YBools: list, CarryIn: bool) -> bool: 
    """Takes input(xxxxxxxx, yyyyyyyy, z) as in x1 + y1 carry in z"""
    X8, X7, X6, X5, X4, X3, X2, X1 = utils.eightBitList_into_individual_bools(XBools)
    Y8, Y7, Y6, Y5, Y4, Y3, Y2, Y1 = utils.eightBitList_into_individual_bools(YBools)

    xout1, adder1out = FOURBITADDERsmall([X4,X3,X2,X1], [Y4,Y3,Y2,Y1], CarryIn)
    xout2, carryout = FOURBITADDERsmall([X8,X7,X6,X5], [Y8,Y7,Y6,Y5], adder1out)

    out4, out3, out2, out1 = utils.fourBitList_into_individual_bools(xout1)
    out8, out7, out6, out5 = utils.fourBitList_into_individual_bools(xout2)
    output = utils.eightIndividualBools_into_eightBitList(out8, out7, out6, out5, out4, out3, out2, out1)

    return output, carryout
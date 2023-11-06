#Name: GatesClass.py
#Author: Aidan Newberry
#Created: 10/14/2023
#Purpose: Define Gates and other Circuts for general use.

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

def NOR_GATE(X1: bool, X2: bool) -> bool:
    """accept two bools and does the OR calculation on them.\n
        Truth Table:\n
        *---------------------*\n
        |INPUT1|INPUT2|OUTPUT1|\n
        |   0  |   0  |   1   |\n
        |   0  |   1  |   0   |\n
        |   1  |   0  |   0   |\n
        |   1  |   1  |   0   |\n
        *---------------------*\n
    """
    #print(f"OR of {X1}, {X2} = {X1 or X2}")
    NOR = (NOT_GATE(OR_GATE(X1,X2)))
    return NOR

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



#not really gates!

#ADDERS
def ADDER(X1: bool, X2: bool, CarryIn: bool) -> bool:
    """Takes input(x, y, z) as in x1 + y1 carry in z"""
    SUM = XOR_GATE(XOR_GATE(X1, X2), CarryIn)
    CARRYOUT = OR_GATE(AND_GATE(XOR_GATE(X1, X2), CarryIn), AND_GATE(X2, X1))

    return [SUM, CARRYOUT]

#made this so i could translate to my logic mask format :)
def TWOBITADDERFORMYSELF(XBools: list, YBools: list, CarryIn: bool)->bool:
    X1, X2 = utils.twoBitList_into_individual_bools(XBools)
    Y1, Y2 = utils.twoBitList_into_individual_bools(YBools)

    xout1 = XOR_GATE(XOR_GATE(X1, Y1), CarryIn)
    xout2 = XOR_GATE(XOR_GATE(X2, Y2), OR_GATE(AND_GATE(XOR_GATE(X1, Y1), CarryIn), AND_GATE(X1, Y1)))
    carryout = OR_GATE(AND_GATE(XOR_GATE(X2, Y2), OR_GATE(AND_GATE(XOR_GATE(X1, Y1), CarryIn), AND_GATE(X1, Y1))), AND_GATE(X2, Y2))

    output = utils.twoIndividualBools_into_twoBitList(xout2, xout1)
    return [output, carryout]

def TWOBITADDER(XBools: list, YBools: list, CarryIn: bool) -> bool:
    """Takes input(xx, yy, z) as in x1 + y1 carry in z"""
    X2, X1 = utils.twoBitList_into_individual_bools(XBools)
    Y2, Y1 = utils.twoBitList_into_individual_bools(YBools)

    xout1, adder1out = ADDER(X1, Y1, CarryIn)
    xout2, carryout = ADDER(X2, Y2, adder1out)

    output = utils.twoIndividualBools_into_twoBitList(xout2, xout1)
    return [output, carryout]

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

    return [output, carryout]

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

    return [output, carryout]



def ALU(XBools: list, YBools: list, Subtract: bool) -> bool:
    """Takes two binary numbers as lists and either adds or subtracts them depending on the 3rd bool input "subtract?"\n
        returns a binary number as a list, and three output bools, carryout, negative and zero: uses a different number system than everything prior to the creation of this gate
    """
    Y4, Y3, Y2, Y1 = utils.fourBitList_into_individual_bools(YBools)

    ADDERout, carryout = FOURBITADDER(XBools, [XOR_GATE(Y4,Subtract),XOR_GATE(Y3,Subtract),XOR_GATE(Y2,Subtract),XOR_GATE(Y1,Subtract)], Subtract)
    
    Z4, Z3, Z2, Z1 = utils.fourBitList_into_individual_bools(ADDERout)

    zero = AND_GATE(AND_GATE(AND_GATE(NOT_GATE(Z4),NOT_GATE(Z3)),NOT_GATE(Z2)),NOT_GATE(Z1))
    negative = Z4
    
    return [ADDERout, carryout, negative, zero] # not shure if i need to have barckets around this


#memory!------------------------
class set_reset_latch():
    """Works as intended, needs to be made as an object because 
    then it will be able to store values. Working example:\n
    
    memory = gate.set_reset_latch()\n

    for i in range(0,3):\n
        \tset = util.get_int("Enter 0 or 1: ")\n
        \treset = util.get_int("Enter 0 or 1: ")\n
        \toutput = memory.Latch(set,reset)\n
        \tprint(f"while set = {set} and reset = {reset}, the output was: {output}")\n

    """
    def __init__(self) -> None:
        self.oldoutput = 0

    def Latch(self, set:bool, reset:bool) -> bool:

        self.output = AND_GATE(OR_GATE(self.oldoutput,set),NOT_GATE(reset))
        self.oldoutput = self.output
        return self.output
    
class data_latch():
    """Works as intended, needs to be made as an object because 
    then it will be able to store values."""

    def __init__(self) -> None:
        self.latch1 = set_reset_latch()

    def datalatch(self, data:bool, store:bool) -> bool:
        output = self.latch1.Latch(AND_GATE(data, store), AND_GATE(NOT_GATE(data), store))
        return output


class DataFlipFlop():
    """needs to be ran as object\n
    
        latch = gate.DataFlipFlop()\n
        for i in range(0,10):\n

            \tX1 = util.get_int("Enter 0 or 1: ")\n
            \tclock = util.get_int("Enter 0 or 1: ")\n
            \toutput = latch.FlipFlop(X1,clock)\n
            \tprint(f"while data = {X1} and clock = {clock}, the output was: {output}")\n

    THIS WORKS! if you feel that it doesnt its because you forgot how it was designed, 
    it only stores data on the rising edge of a pulse meaning if the clock pin 
    isnt chainging from 0 to 1 it wont do anything 
    """

    def __init__(self) -> None:
        self.latch1 = data_latch()
        self.latch2 = data_latch()
        self.oldclock = 0

    def FlipFlop(self, data:bool, clock:bool) -> bool:

        output = self.latch2.datalatch(self.latch1.datalatch(data, NOT_GATE(self.oldclock)),clock)
        self.oldclock = clock
        return output


class SynchronousRegister():
    """a register that stores data only when the store signle is on and when the rising edge of the clock happens!"""
    def __init__(self) -> None:
        self.flipflop1 = DataFlipFlop()
        self.outputnew = 0

    def register(self, data:bool, store:bool, clock:bool) -> bool:
        self.outputold = self.outputnew

        OR = OR_GATE(AND_GATE(self.outputold, NOT_GATE(store)), AND_GATE(data, store))
        self.outputnew = self.flipflop1.FlipFlop(OR, clock)

        return self.outputnew 
    

class four_bit_register():
    """Example code to run this:
    
        register = gate.four_bit_register()\n

        while True == True:\n
            X4 = util.get_int("Enter 0 or 1: ")\n
            X3 = util.get_int("Enter 0 or 1: ")\n
            X2 = util.get_int("Enter 0 or 1: ")\n
            X1 = util.get_int("Enter 0 or 1: ")\n
            print(f"input = {[X4, X3, X2, X1]}")\n

            store = util.get_int("Enter 0 or 1: ")\n

            clock = util.get_int("Enter 0 or 1: ")\n

            output = register.four_bit_register([X4, X3, X2, X1],store, clock)\n
            
            print(f"output = {output}")\n
    """
    def __init__(self) -> None:
        self.register4 = SynchronousRegister()
        self.register3 = SynchronousRegister()
        self.register2 = SynchronousRegister()
        self.register1 = SynchronousRegister()

    def four_bit_register(self, Xbits:list, store:bool, clock:bool) -> list:
        X1, X2, X3, X4 = utils.fourBitList_into_individual_bools(Xbits)

        Xout4 = self.register4.register(X4, store, clock)
        Xout3 = self.register3.register(X3, store, clock)
        Xout2 = self.register2.register(X2, store, clock)
        Xout1 = self.register1.register(X1, store, clock)

        Xoutbits = utils.fourIndividualBools_into_fourBitList(Xout4, Xout3, Xout2, Xout1)
        return Xoutbits

#seven segment display, should work if im not too dumb to setup all the functions
def sevensegdisplaydriver(Xlist:list) -> list:
    X1, X2, X3, X4 = utils.fourBitList_into_individual_bools(Xlist)

    output1 = X4

    output2 = OR_GATE(XOR_GATE((XOR_GATE(X4,X3)),(NOR_GATE(X4,OR_GATE(X2, X1)))),(OR_GATE(AND_GATE(OR_GATE(XOR_GATE(X3,X2),NOT_GATE(X1)),X1),NOR_GATE(NOR_GATE(NOT_GATE(X3),X2),X1))))
    
    output3 = NAND_GATE(AND_GATE(XOR_GATE(X4,X3),OR_GATE(X2,X1)), OR_GATE(X2,X1))
    
    output4 = OR_GATE(NAND_GATE(NAND_GATE(AND_GATE(XOR_GATE(X4,X3),OR_GATE(X2,X1)), OR_GATE(X2,X1)),OR_GATE(X2, X1)), X1)
    
    output5 = OR_GATE(AND_GATE(OR_GATE(XOR_GATE(X3,X2),NOT_GATE(X1)),X1),NOR_GATE(NOR_GATE(NOT_GATE(X3),X2),X1))
    
    output6 = NOR_GATE(NOR_GATE(NOT_GATE(X3),X2),X1)
    
    output7 = NAND_GATE(NAND_GATE(AND_GATE(XOR_GATE(X4,X3),OR_GATE(X2,X1)), OR_GATE(X2,X1)),OR_GATE(X2, X1))
    
    output8 = OR_GATE(XOR_GATE(NOR_GATE(X4,OR_GATE(X2,X1)),OR_GATE(XOR_GATE(X3,X2),NOT_GATE(X1))),NOR_GATE(NOT_GATE(X3),X2))

    finoutput = [output1, output2, output3, output4, output5, output6, output7, output8,]

    return finoutput


#extra stuff that doenst even matter
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

def SixTeenBitAdderSmall(XBools: list, YBools: list, CarryIn: bool) -> bool: 
    X16, X15, X14, X13, X12, X11, X10, X9, X8, X7, X6, X5, X4, X3, X2, X1 = utils.sixteenBitList_into_individualbools(XBools)
    Y16, Y15, Y14, Y13, Y12, Y11, Y10, Y9, Y8, Y7, Y6, Y5, Y4, Y3, Y2, Y1 = utils.sixteenBitList_into_individualbools(YBools)
    
    xout1, adder1out = EIGHTBITADDERsmall([X8, X7, X6, X5, X4, X3, X2, X1], [Y8, Y7, Y6, Y5, Y4, Y3, Y2, Y1], CarryIn)
    xout2, carryout = EIGHTBITADDERsmall([X16, X15, X14, X13, X12, X11, X10, X9], [Y16, Y15, Y14, Y13, Y12, Y11, Y10, Y9], adder1out)
    
    out8, out7, out6, out5, out4, out3, out2, out1 = utils.eightBitList_into_individual_bools(xout1)
    out16, out15, out14, out13, out12, out11, out10, out9 = utils.eightBitList_into_individual_bools(xout2)
    output = utils.sixteenindividualbools_into_sixteenbitlist(out16, out15, out14, out13, out12, out11, out10, out9, out8, out7, out6, out5, out4, out3, out2, out1)

    return output, carryout

def ThirtytwoBitAdderSmall(XBools: list, YBools: list, CarryIn: bool) -> bool: 
    X32, X31, X30, X29, X27, X27, X26, X25, X24, X23, X22, X21, X20, X19, X18, X17, X16, X15, X14, X13, X12, X11, X10, X9, X8, X7, X6, X5, X4, X3, X2, X1 = utils.thirtytwobitlist_into_thirtytwoindividualbools(XBools)
    Y32, Y31, Y30, Y29, Y27, Y27, Y26, Y25, Y24, Y23, Y22, Y21, Y20, Y19, Y18, Y17, Y16, Y15, Y14, Y13, Y12, Y11, Y10, Y9, Y8, Y7, Y6, Y5, Y4, Y3, Y2, Y1 = utils.thirtytwobitlist_into_thirtytwoindividualbools(YBools)

    xout1, adder1out = SixTeenBitAdderSmall([X16, X15, X14, X13, X12, X11, X10, X9, X8, X7, X6, X5, X4, X3, X2, X1],[Y16, Y15, Y14, Y13, Y12, Y11, Y10, Y9, Y8, Y7, Y6, Y5, Y4, Y3, Y2, Y1],CarryIn)
    xout2, carryout = SixTeenBitAdderSmall([X32, X31, X30, X29, X27, X27, X26, X25, X24, X23, X22, X21, X20, X19, X18, X17],[Y32, Y31, Y30, Y29, Y27, Y27, Y26, Y25, Y24, Y23, Y22, Y21, Y20, Y19, Y18, Y17],adder1out)

    out16, out15, out14, out13, out12, out11, out10, out9, out8, out7, out6, out5, out4, out3, out2, out1 = utils.sixteenBitList_into_individualbools(xout1)
    out32, out31, out30, out29, out28, out27, out26, out25, out24, out23, out22, out21, out20, out19, out18, out17 = utils.sixteenBitList_into_individualbools(xout2)
    output = utils.thirtyTwoindividualbools_into_thirtytwobitlist(out32, out31, out30, out29, out28, out27, out26, out25, out24, out23, out22, out21, out20, out19, out18, out17, out16, out15, out14, out13, out12, out11, out10, out9, out8, out7, out6, out5, out4, out3, out2, out1)

    return output, carryout

def SixtyFourBitADDERSmall(XBools: list, YBools: list, CarryIn: bool) -> bool:
    X64, X63, X62, X61, X60, X59, X58, X57, X56, X55, X54, X53, X52, X51, X50, X49, X48, X47, X46, X45, X44, X43, X42, X41, X40, X39, X38, X37, X36, X35, X34, X33, X32, X31, X30, X29, X27, X27, X26, X25, X24, X23, X22, X21, X20, X19, X18, X17, X16, X15, X14, X13, X12, X11, X10, X9, X8, X7, X6, X5, X4, X3, X2, X1 = utils.sixtyfourbitlist_into_sixtyfourindividualbools(XBools)
    Y64, Y63, Y62, Y61, Y60, Y59, Y58, Y57, Y56, Y55, Y54, Y53, Y52, Y51, Y50, Y49, Y48, Y47, Y46, Y45, Y44, Y43, Y42, Y41, Y40, Y39, Y38, Y37, Y36, Y35, Y34, Y33, Y32, Y31, Y30, Y29, Y27, Y27, Y26, Y25, Y24, Y23, Y22, Y21, Y20, Y19, Y18, Y17, Y16, Y15, Y14, Y13, Y12, Y11, Y10, Y9, Y8, Y7, Y6, Y5, Y4, Y3, Y2, Y1 = utils.sixtyfourbitlist_into_sixtyfourindividualbools(YBools)

    xout1, adder1out = ThirtytwoBitAdderSmall([X32, X31, X30, X29, X27, X27, X26, X25, X24, X23, X22, X21, X20, X19, X18, X17, X16, X15, X14, X13, X12, X11, X10, X9, X8, X7, X6, X5, X4, X3, X2, X1],[Y32, Y31, Y30, Y29, Y27, Y27, Y26, Y25, Y24, Y23, Y22, Y21, Y20, Y19, Y18, Y17, Y16, Y15, Y14, Y13, Y12, Y11, Y10, Y9, Y8, Y7, Y6, Y5, Y4, Y3, Y2, Y1],CarryIn)
    xout2, carryout = ThirtytwoBitAdderSmall([X64, X63, X62, X61, X60, X59, X58, X57, X56, X55, X54, X53, X52, X51, X50, X49, X48, X47, X46, X45, X44, X43, X42, X41, X40, X39, X38, X37, X36, X35, X34, X33],[Y64, Y63, Y62, Y61, Y60, Y59, Y58, Y57, Y56, Y55, Y54, Y53, Y52, Y51, Y50, Y49, Y48, Y47, Y46, Y45, Y44, Y43, Y42, Y41, Y40, Y39, Y38, Y37, Y36, Y35, Y34, Y33],adder1out)

    out32, out31, out30, out29, out28, out27, out26, out25, out24, out23, out22, out21, out20, out19, out18, out17, out16, out15, out14, out13, out12, out11, out10, out9, out8, out7, out6, out5, out4, out3, out2, out1 = utils.thirtytwobitlist_into_thirtytwoindividualbools(xout1)
    out64, out63, out62, out61, out60, out59, out58, out57, out56, out55, out54, out53, out52, out51, out50, out49, out48, out47, out46, out45, out44, out43, out42, out41, out40, out39, out38, out37, out36, out35, out34, out33 = utils.thirtytwobitlist_into_thirtytwoindividualbools(xout2)
    output = utils.sixtyfourindividualbools_into_sixtyfourbitlist(out64, out63, out62, out61, out60, out59, out58, out57, out56, out55, out54, out53, out52, out51, out50, out49, out48, out47, out46, out45, out44, out43, out42, out41, out40, out39, out38, out37, out36, out35, out34, out33, out32, out31, out30, out29, out28, out27, out26, out25, out24, out23, out22, out21, out20, out19, out18, out17, out16, out15, out14, out13, out12, out11, out10, out9, out8, out7, out6, out5, out4, out3, out2, out1)
    
    return output, carryout
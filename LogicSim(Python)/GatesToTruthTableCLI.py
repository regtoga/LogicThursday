#Name: GatesToTruthTable.py
#Author: Aidan Newberry
#Created: 10/6/2023
#Purpose: CLI to turn a predefined Gate array into a TruthTable.

import GatesClass as gate
import utilsV1 as utils

def main():

    #dimentionsgate = GetDimentionsOfGateCLI()
    dimentionsgate = [[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0]]]
    print(dimentionsgate)

    somewierdlist = WhatGateCLI(dimentionsgate)

    print("")

def WhatGateCLI(GateDimentions: list) -> list:
    """
    User will choose a gate to test and using the GateDimentions provided it will 
    iterate though every possible way the gate could be executed
    """
    
    intgatechosen = utils.get_int("Enter integer code for the gate you want to find the truth table for: ")

    #Example dimentions: [[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0]]]
        
    #Example Combinations List: [[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0,0,0,0],[1]],[[0,0,0,0],[0,0,0,1],[0]]]
    combinations = [[]]

    #finds the largest number representable in binary using the ammount of zeros present in the inputs
    Xdimentions = len(GateDimentions[0])
    Xwidth = 0
    for dimention in range(0, Xdimentions):
        Xwidth += len(GateDimentions[0][dimention])
    Larestnumberpossiblebylength = 2**Xwidth
    print(f"Combinations possible: {Larestnumberpossiblebylength}")

    #Find every possible combination
    for num in range(0, Larestnumberpossiblebylength):
        binarynumber = bin(num)
        templist = []
        
        for binnum in range(1, len(binarynumber)):
            if binarynumber[-binnum] == 'b':
                break
            else:
                if binarynumber[-binnum] == '0':
                    templist.append(0)
                elif binarynumber[-binnum] == '1':
                    templist.append(1)
                

        #print(f"{templist}, {len(templist)} long")

    
        while len(templist) < Xwidth:
            templist.append(0)

        print(f"{templist}, {len(templist)} long")

    Gates = {
        1: gate.AND_GATE(1,1),
        2: gate.NOT_GATE(1),
        3: gate.OR_GATE(1,1),
        4: gate.NAND_GATE(1,1),
        5: gate.XOR_GATE(1,1),
        6: gate.ADDER(1,1,1),
        7: gate.TWOBITADDER([1,1],[1,1],1),
        8: gate.FOURBITADDER([1,1,1,1],[1,1,1,1],1),
        9: gate.EIGHTBITADDER([1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],1), 
    }

    #Gates.get(intgatechosen, "didnt work :(")

    return 0


def GetDimentionsOfGateCLI() -> list:
    """Will ask user a few questions before returning a list descrbing the dimentions of a gate"""
    #EX: [[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0]]]
    #D1 = inputs and outputs
    #D2 = ammount of inputs and outputs
    #D3 = ammount of bits per input and output

    dimentions = [[],[]]

    inputs = utils.get_int("How many inputs does this gate have?: ")
    outputs = utils.get_int("Ok Thanks! now how many outputs does this gate have?: ")

    
    for input in range(0, inputs):
        #for each input in inputs:
        #Get ammount of input bits
        inputbits = utils.get_int(f"How many input bits for input {input + 1}: ")
        #make a net list to later append ammount of input bits to, later it will be appended to the correct spot in the dimentions list
        inputbitlist = []
        for bit in range(0, inputbits):
            #For each bit in inputbits:
            inputbitlist.append(0)
        #append the ammount of input bits the end end of the dimentions list
        dimentions[0].append(inputbitlist)

    #literally the same as the input loop
    for output in range(0, outputs):
        outputbits = utils.get_int(f"How many output bits for output {output + 1}: ")
        outputbitlist = []
        for bit in range(0, outputbits):
            outputbitlist.append(0)
        dimentions[1].append(outputbitlist)

    return dimentions

if __name__ == "__main__":
    main()

#Name: GatesToTruthTable.py
#Author: Aidan Newberry
#Created: 10/6/2023
#Purpose: CLI to turn a predefined Gate array into a TruthTable.

import GatesClass as gate
import utilsV1 as utils

def main():
    #print all gate types
    print(" (1) NOT: \n (2) SevenSegdisplayDriver: \n (3) AND: \n (4) OR: \n (5) NOR \n (6) NAND: \n (7) XOR: \n (8) ADDER: \n (9) TWOBITADDER \n (10) FOURBITADDER \n (11) EIGHTBITADDER \n (12) ALU \n")

    Combinations, results = WhatGateCLI()

    comboformat = utils.individualInput_into_TruthTableFormat(Combinations)
    resultsformat = utils.individualInput_into_TruthTableFormat(results)
    truthTable = utils.format_truth_table(comboformat, resultsformat)
    print(f"length of Combinations = {len(Combinations)} AND length of results = {len(results)}")
    print(truthTable)

def WhatGateCLI() -> list:
    """
    User will choose a gate to test and using the GateDimentions provided it will 
    iterate though every possible way the gate could be executed
    """
    intgatechosen = utils.get_int("Enter integer code for the gate you want to find the truth table for: ")

    GateDimentionValues = {
        1:[[[0]],[[0]]],
        2:[[[0,0,0,0]],[[0],[0],[0],[0],[0],[0],[0],[0]]],
        3:[[[0],[0]],[[0]]],
        4:[[[0],[0]],[[0]]],
        5:[[[0],[0]],[[0]]],
        6:[[[0],[0]],[[0]]],
        7:[[[0],[0]],[[0]]],
        8:[[[0],[0],[0]],[[0],[0]]],
        9:[[[0,0],[0,0],[0]],[[0,0],[0]]],
        10:[[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0]]],
        11:[[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0]],[[0,0,0,0,0,0,0,0],[0]]],
        12:[[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0],[0],[0]]]
    }

    GateDimentions = GateDimentionValues.get(intgatechosen, f"{intgatechosen} did not correspond to a built in gate.")
    print(GateDimentions)
    if GateDimentions == f"{intgatechosen} did not correspond to a built in gate.":
        print("You must correct your actions by imputing your own gate mask!")
        GateDimentions = GetDimentionsOfGateCLI()

    #Example dimentions: [[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0]]]
        
    #Example Combinations and results List: [[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0,0,0,0],[1]],[[0,0,0,0],[0,0,0,1],[0]]]
    combinations = []
    results = []

    #finds the largest number representable in binary using the ammount of zeros present in the inputs
    Xdimentions = len(GateDimentions[0])
    Xwidth = 0
    Xwidthlist = []
    for dimention in range(0, Xdimentions):
        Xwidth += len(GateDimentions[0][dimention])
        Xwidthlist.append(len(GateDimentions[0][dimention]))
    Larestnumberpossiblebylength = 2**Xwidth
    #print(f"Combinations possible: {Larestnumberpossiblebylength}")

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

        #converter regular binary to what i need
        while len(templist) < Xwidth:
            templist.append(0)

        #iterate though all the inputs
        
        index = 0

        combinations.append([])
        results.append([])

        for input in range(0, len(Xwidthlist)):
            #should make a list that looks like this: [[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0,0,0,0],[1]],[[0,0,0,0],[0,0,0,1],[0]]]
            evenTemperList = []


            for inputlenght in range(0, Xwidthlist[input]):
                evenTemperList.append(templist[index])

                index += 1

            combinations[num].append(evenTemperList)

        #start actually turning each combination into a result
        #for gates that take only a bool we need to add another [0] pointer so that it will return a bool and not a list
        if intgatechosen == 1:
            results[num].append([gate.NOT_GATE(combinations[num][0][0])])
        elif intgatechosen == 2:
            results[num].append([gate.sevensegdisplaydriver(combinations[num][0])])
        elif intgatechosen == 3:
            results[num].append([gate.AND_GATE(combinations[num][0][0],combinations[num][1][0])])
        elif intgatechosen == 4:
            results[num].append([gate.OR_GATE(combinations[num][0][0],combinations[num][1][0])])
        elif intgatechosen == 5:
            results[num].append([gate.NOR_GATE(combinations[num][0][0],combinations[num][1][0])])
        elif intgatechosen == 6:
            results[num].append([gate.NAND_GATE(combinations[num][0][0],combinations[num][1][0])])
        elif intgatechosen == 7:
            results[num].append([gate.XOR_GATE(combinations[num][0][0],combinations[num][1][0])])
        elif intgatechosen == 8:
            results[num].append(gate.ADDER(combinations[num][0][0],combinations[num][1][0],combinations[num][2][0]))
        elif intgatechosen == 9:
            results[num].append(gate.TWOBITADDER(combinations[num][0],combinations[num][1],combinations[num][2][0]))
        elif intgatechosen == 10:
            results[num].append(gate.FOURBITADDER(combinations[num][0],combinations[num][1],combinations[num][2][0]))
        elif intgatechosen == 11:
            results[num].append(gate.EIGHTBITADDER(combinations[num][0],combinations[num][1],combinations[num][2][0]))
        elif intgatechosen == 12:
            results[num].append(gate.ALU(combinations[num][0],combinations[num][1],combinations[num][2][0]))  

    return combinations, results


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

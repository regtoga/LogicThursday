#Name: GatesToTruthTable.py
#Author: Aidan Newberry
#Created: 10/6/2023
#Purpose: CLI to turn a predefined Gate array into a TruthTable.

import utilsV1 as utils
import GataDataFunctions as GateData


def main(anyExports:bool=False, ManualGateMaskSubmisson:bool=False):

    archie = utils.fileArchitect()

    #print all gate types
    GateData.PrintAllGateTypes()
    Combinations, results, GateDimentions = WhatGateCLI(anyExports, ManualGateMaskSubmisson)

    comboformat = utils.individualInput_into_TruthTableFormat(Combinations)
    resultsformat = utils.individualInput_into_TruthTableFormat(results)
    truthTable = utils.format_truth_table(comboformat, resultsformat)
    print(f"length of Combinations = {len(Combinations)} AND length of results = {len(results)}")
    if len(Combinations) < 100:
        print(truthTable)

    if anyExports == True:

        export = input("Do you want to export formatted results into a text file? (Y/N)")
        if export == "Y" or export == "y":
            default = input("Do you want to use default file location and name? (Y/N)")

            locationfromuser = ""
            filenamefromuser = ""

            if default == "N" or default == "n":
                filenamefromuser = input("Enter the name you want for you text file: EX(banan) becomes banan.txt: ")
                locationfromuser = input("Enter a location for your txt file: EX(D:\windows folders\Downloads\) \nI would recomend leaving this blank:")
                

            print(archie.Create_File(locationfromuser, filenamefromuser, Combinations))
            print(archie.Write_File(truthTable))

            exit()
    
    return [Combinations, results], GateDimentions

def WhatGateCLI(anyExports, ManualGateMaskSubmisson) -> list:
    """
    User will choose a gate to test and using the GateDimentions provided it will 
    iterate though every possible way the gate could be executed
    """

    intgatechosen = utils.get_int("Enter integer code for the gate you want to find the truth table for: ")

    #GateData.GateDimentionValuesfunction is a function that will return GateDimentions weather the gate the user wants is predefined or not.
    #Example dimentions: [[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0]]]
    GateDimentions = GateData.GateDimentionValuesfunction(intgatechosen)

    #allows submission of truthtable though the CLI
    if intgatechosen == 0 and ManualGateMaskSubmisson == False:

        #You should add functionality where if the truth table is valid, automatically generate GateDimentions!
        while True:
            TruthTable = input("Enter a truthTable manually or by pointing to a file: ")

            TruthTable = utils.convert_string_to_list(TruthTable)


            if TruthTable != None:
                try:
                    if type(TruthTable[0][0][0]) == list and type(TruthTable[0][0][1] == list):
                        print("Valid TruthTable, Moving on!")
                        combinations = TruthTable[0]
                        results = TruthTable[1]
                        return combinations, results, GateDimentions
                except:
                    print("That TruthTable sucked lol.")
            else:
                print("I havent added Manually pointing to a file yet! :) ttyl.")


    if ManualGateMaskSubmisson == True:
            while True:
                UserInputMask = input("Enter a Mask in maunally or by pointing to a file: ")

                UserInputMask = utils.convert_string_to_list(UserInputMask)

                if UserInputMask != None:
                    try:
                        if type(UserInputMask[0]) == str and type(UserInputMask[1]) == list and type(UserInputMask[2]) == list:


                            print("Please DADDY FIX ME!!!")


                            continue
                    except:
                        print("That wasnt right")

    
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

        for input2 in range(0, len(Xwidthlist)):
            #should make a list that looks like this: [[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0,0,0,0],[1]],[[0,0,0,0],[0,0,0,1],[0]]]
            evenTemperList = []


            for inputlenght in range(0, Xwidthlist[input2]):
                evenTemperList.append(templist[index])

                index += 1

            combinations[num].append(evenTemperList)

        #start actually turning each combination into a result
        #for gates that take only a bool we need to add another [0] pointer so that it will return a bool and not a list
        #GateData.ChooseGateToUse is a fancy function that takes some of the edge off of making adding a new hardcoded gate
        gateanswer = GateData.ChooseGateToUse(intgatechosen, combinations, num)
        results[num].append(gateanswer)

    #Export Raw TruthTable, this gets skipped if user enters his own raw truthTable
    if anyExports == True:
        #ask if user wants raw truthtable
        rawTruthTable = utils.get_int("Do you want the raw truthtable: (0 = NO | 1 = YES): ")

        if rawTruthTable == 1:
            rawTruthTableArchie = utils.fileArchitect()
            default = utils.get_int("Do you want to use default file location and name? (0 = NO | 1 = YES): ")

            locationfromuser = ""
            formatfilename = (GateData.GetGateName(intgatechosen).replace(" ", "")).replace("\n", "")

            filenamefromuser = f"rawtruthtablefor-{formatfilename}"

            if default == 0:
                filenamefromuser = input("Enter the name you want for you text file: EX(banan) becomes banan.txt: ")
                locationfromuser = input("Enter a location for your txt file: EX(D:\windows folders\Downloads\) \nI would recomend leaving this blank:")
                

            print(rawTruthTableArchie.Create_File(locationfromuser, filenamefromuser, [combinations, results]))
            print(rawTruthTableArchie.Write_File([combinations, results]))


    return combinations, results, GateDimentions


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
    userinput = 0
    while True:
        userinput = utils.get_int("What type of input do you have? Mask(1) or RawTable(2): ")

        if userinput == 1:
            main(True)
        if userinput == 2:
            main(True, True)

    

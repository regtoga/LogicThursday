"""
Make a function that when given a mask EX:([[[0,0,0,0]],[[0],[0],[0],[0],[0],[0],[0],[0]]]) or ([[[0],[0],[0]],[[0],[0]]]) and a truthtable ex:

0|0|0|0||0|1|1|1|1|1|1|0        0|0|0||0|0
1|0|0|0||1|1|1|1|1|1|1|1        1|0|0||1|0
0|1|0|0||0|0|1|1|0|0|1|1        0|1|0||1|0
1|1|0|0||1|0|1|1|0|0|1|1        1|1|0||0|1
0|0|1|0||0|1|1|0|1|1|0|1        0|0|1||1|0
1|0|1|0||1|1|0|1|1|1|1|1        1|0|1||0|1
0|1|1|0||0|1|0|1|1|1|1|1        0|1|1||0|1
1|1|1|0||1|1|1|0|1|1|0|1        1|1|1||1|1 
0|0|0|1||0|0|1|1|0|0|0|0
1|0|0|1||1|1|0|1|0|0|1|0
0|1|0|1||0|1|0|1|1|0|1|1
1|1|0|1||1|1|1|1|1|0|0|1
0|0|1|1||0|1|1|1|1|0|0|1
1|0|1|1||1|1|0|1|1|0|1|1
0|1|1|1||0|1|0|1|0|0|1|0
1|1|1|1||1|0|1|1|0|0|0|0

... The function will generate the nessesary logic needed,

There are many ways to optimise this problem, such as minimum ammount of gates, what types of gates can be used, wire length, and time to execute. But for the first
iteration of this program i am just going to see if i can make it work! (meaning brute force) but (i still want to be able to choose what types of gates its allowed to use)


To make the function i want to also have a gate type mask, what this mask will do is using the GateDataFunctions data it will determing what gates it can use.
Ex: we input a list that looks like this [1(NOT), 3(AND), 4(OR), 5(NOR)] and it will only be able to attempt a solution out of those gates


----

to actually solve the problem i think i can generate possible combinations of gates. I need to write a function that takes a io mask, truthtable, and seed then returns an a possible solution in need of validation EX:
Name:              ADDER
input/output mask: [[[0],[0],[0]],[[0],[0]]]
Truthtable:        [[0], [1], [1]], [[1], [1], [1]]], [[(0, 0)], [(1, 0)], [(1, 0)], [(0, 1)], [(1, 0)], [(0, 1)], [(0, 1)], [(1, 1)]]]
GateMask:          [3, 4, 7]

OUTPUT:
Name: ADDER
input = X1, X2, X3
Outputs = Y1, Y2
gate format [name, [inputs], [outputs, [Logic]]]
Potential gate = [ADDER,[[[X1,#]], [[X2,#]], [[X3,#]]],[[[Y1,[7,[[7,[X1,X2]],X3]]]],[[Y2, [Y2, [4,[[3,[[7,[X1,X2]],X3]],[3,[X2,X1]]]]]]],]]
or
[
    ADDER, 
    [
        [
            X1, #
        ], 
        [
            X2, #
        ], 
        [
            X3, #
        ]
    ],
    [
        [
            [Y1,[Logic]] #SUM
        ], 
        [
            [Y2, [Logic]] #Carry Out
        ]
    ]
]

TruthTableToGates INPUTS:
1. input/output mask
2. Truthtable
3. GateMask

TruthTableToGates OUTPUTS:
3. array of gates using format of input/output mask
"""

import time

import GatesClass
import GataDataFunctions
import GatesToTruthTableCLI
import utilsV1


class TruthTableToGatesCLI():
    def __init__(self) -> None:
        pass
    
    def logicMaskMaker(inputmask:list, inputgatemask:list, TruthTable:list, name:str="UserCreatedGate", depthmask:list=[1,10], timelimit:int=10):
        """Takes in a input mask ([[[0],[0],[0]],[[0],[0]]]) and creates the logic mask ([Y2, [Logic]]) based on a the inputGateMask, and depth mask
            the depth mask is just a way for the program to know the range of depth its allowed to search up to for each function, [Y1, []].
            If i do one input at a time and stop searching for that input when it finds the correct var, it should be MUCH quicker than if i dont.
        """
        HardlogicMask = ["ADDER",[["X1","bool"], ["X2","bool"], ["X3","bool"]],[["Y1",[7,[[7,["X1","X2"]],"X3"]]],["Y2",[4,[[3,[[7,["X1","X2"]],"X3"]],[3,["X2","X1"]]]]]]]
        
        logicMask = [name,[],[]]

        justinputsfromIOmask = inputmask[0]
        justoutputsfromIOmask = inputmask[1]

        inputnum = 1
        for input in justinputsfromIOmask:
            if len(input) > 1:
                logicMask[1].append([f"X{inputnum}","list"])
            else:
                logicMask[1].append([f"X{inputnum}","bool"])
            inputnum += 1

        outputnum = 1
        for output in justoutputsfromIOmask:
            logicMask[2].append([f"Y{outputnum}",[]])
            outputnum += 1    

        internalTimeTaken = time.time()
        logicMasks = []
        print(f"Starting mask = {logicMask}")
        while True:
            #code goes here

            #temp logic mask maker... NEEDS TO BE REPLACED WITH A FUNCTION THAT GENERATES 
            # THE OUTPUTS AND APPENDS EACH OF THEM INDIVIDUALLY TO THE LOGIC MASK
            logicMask = HardlogicMask

            #Gates were allowed to use when generating an answer:
            inputgatemask = inputgatemask
            
            #temp way to iterate though the outputs.
            #What should happen is after one of the inputs is generated it will be validated if it is false it will generate a new input,
            #Once it is done it will go to the next input, should reduce headway
            outputslist = []
            for outputs in range(1, len(justoutputsfromIOmask)+1):
                
                masksingleResult = TruthTableToGatesCLI.logicMaskValidator(logicMask, TruthTable, outputs)
                outputslist.append(masksingleResult)
                
                if masksingleResult == 0:
                    break

            

            #code ends here
            maskResults = 0  

            for outputsingle in outputslist:
                if outputsingle != 0:
                    maskResults = 1

            if maskResults == 1:
                #determing if mask already has been found
                inside = False
                for logicMasK in logicMasks:
                   if logicMasK == logicMask:
                       inside = True
                       continue 

                if inside == False:
                    logicMasks.append(logicMask)

                    print("Found one!")
                    #Doesnt actually work
                    #Determing if the gate is too large to nicely fit on the screen
                    if True == True:
                        print(f"It looked like\n{logicMask}\n")
                        
                    contineTheSearch = utilsV1.get_int("Do you want to continue searching for more valid answers? (1 = yes, 0 = no): ")
                    if contineTheSearch == 0:
                        return f"LogicMasks were: \n{logicMasks}\n"
                    internalTimeTaken = time.time()
                

                
            elif time.time() - internalTimeTaken > timelimit:
                contineTheSearch = utilsV1.get_int("Nothing has happend in a while... want to continue searching? (1 = yes, 0 = no): ")
                if contineTheSearch == 0:
                    return f"LogicMasks were: \n{logicMasks}\n"
                internalTimeTaken = time.time()

    #----------------------------------- function should try all combinations of the program and compare the ouput with the truth table
    def logicMaskValidator(logicMask:list="", TruthTable:list="", TestThisInput:int=0) -> bool:
        """gate format [name, [inputs], [outputs, [Logic]]]
        returns true or false depending on if the logic mask actually fufills the desired outcome"""

        if logicMask == "" or TruthTable == "":
            return False

        logicOut = []

        #name = logicMask[0]
        #inputs = logicMask[1]
        outputsANDlogic = logicMask[2]

        #will only test for one of the nessesary fields
        if TestThisInput != 0:
            outputsANDlogic = [logicMask[2][TestThisInput-1]]
            for truthtablelen in range(0, len(TruthTable[0])):
                
                currentlogicOut = [[]]

                for outputletters in outputsANDlogic:
                    currentlist = outputletters

                    gateinputs = TruthTableToGatesCLI.variableUnifier(TruthTable[0][truthtablelen])

                    currentanswer = TruthTableToGatesCLI.outputLogicator(currentlist[1], gateinputs)

                    currentlogicOut[0].append(currentanswer)

                logicOut.append(currentlogicOut)

                currentTruthTableUnified = [TruthTableToGatesCLI.variableUnifier([TruthTable[1][truthtablelen][0][TestThisInput-1]])]

                if currentlogicOut == currentTruthTableUnified:
                    continue
                else:
                    return 0
            return 1


        #this loops for every different input inside ofe the truthTable inputs side
        for truthtablelen in range(0, len(TruthTable[0])):
            #This portion of the code needs to take the outputsandlogic into consideration and actually execute the code
            #EX mask [['Y1', [7, [[7, ['X1', 'X2']], 'X3']]], ['Y2', [4, [[3, [[7, ['X1', 'X2']], 'X3']], [3, ['X2', 'X1']]]]]]
            currentlogicOut = [[]]
            for outputletters in outputsANDlogic:
                currentlist = outputletters

                gateinputs = TruthTableToGatesCLI.variableUnifier(TruthTable[0][truthtablelen])

                #print("-"*30)
                #print(f"current list{currentlist[1]}\nGate inputs{gateinputs}\n")
                currentanswer = TruthTableToGatesCLI.outputLogicator(currentlist[1], gateinputs)

                currentlogicOut[0].append(currentanswer)

            #print("-"*30)
            logicOut.append(currentlogicOut)

            #short circuts the function if it finds something that doesnt work
            currentTruthTableUnified = [TruthTableToGatesCLI.variableUnifier(TruthTable[1][truthtablelen][0])]

            if currentlogicOut == currentTruthTableUnified:
                #print(f"Gate inputs{gateinputs}")
                #print(f"is:{currentlogicOut}")
                #print(f"Supposed to be:{currentTruthTableUnified}")
                continue
            else:
                #print(f"Gate inputs{gateinputs}")
                #print(f"is:{currentlogicOut}")
                #print(f"Supposed to be:{currentTruthTableUnified}\n")
                return 0
            

        #returns 1 if correct and 0 if not
        if logicOut == TruthTable[1]:
            return 1
        else:
            return 0


    def outputLogicator(logicIn:list, variablesIn:list):
        """
        a function that takes something that looks like this as input:
        [7, [7, ['X1', 'X2']], 'X3'] or [4, [[3, [[7, ['X1', 'X2']], 'X3']], [3, ['X2', 'X1']]]]
        """
        answer = "nothing"
        opperation = logicIn[0]

        data = []
        for logic in logicIn[1]:
            data.append(logic)

    
        #two different variables go though the same function and it returns their values, probbly easily expandible to more vars?
        X1 = "nothing"
        X1, data = TruthTableToGatesCLI.inputFinder(data, variablesIn, opperation, 1)

        X2 = "nothing"
        if len(data) == 2: 
            X2, data = TruthTableToGatesCLI.inputFinder(data, variablesIn, opperation, 2)

        answer = GataDataFunctions.GatesAvailable(opperation,X1,X2)
        #print(f"LogicIn: {logicIn}\nCurrentData: {data}\nopperation: {opperation}, X1: {X1}, X2: {X2}, answer: {answer} \n")
        return answer
    
    def inputFinder(data:list, variables:list, opperation, inputnum:int):
        """allows for the creation of more variables to search though at a time by method(ifying) the variable search"""
        X = "nothing"
        inputnum = inputnum - 1
        if type(data[inputnum]) == str:
            X = int(data[inputnum].replace("X",""))
            X = variables[X-1]

            data[inputnum] = X

        elif type(opperation) == int:
            data[inputnum] = TruthTableToGatesCLI.outputLogicator(data[inputnum], variables)
            X = data[inputnum]
        return X, data

    def variableUnifier(variables:list):
        """a function to unify different types of 2d lists
        [[0], [0], [0]] -> [0, 0, 0]
        [[0, 0, 0, 0]] -> [0, 0, 0, 0]
        [[0, 0], [0, 0], [0]] -> [0, 0, 0, 0, 0]
        [[0, 0], 0] -> [0, 0, 0]"""
        output = []

        for var in variables:
            if type(var) == list:
                for varinvar in var:
                    output.append(varinvar)
            else:
                output.append(var)
        
        #print(f"{variables} len(variables) = {len(variables)} output = {output}")
        
        return output
    
    def GateTypeSelectorCLI():
        AvailableGateLocatorValues = [0,1,3,4,5,6,7]
        ChosenGateLocatorValues = []

        while True:
            print("")
            prompt = ""

            for value in AvailableGateLocatorValues:
                if value == 0:
                    prompt += "(0) Do Nothing\n"
                else:
                    prompt += GataDataFunctions.GetGateName(value)
            
            prompt += "(10) Finish/Submit"
            prompt += "\nEnter the int values for the gates you would like to allow used in-\nyour logic: "

            gateUserWants = utilsV1.get_int(prompt)
            if gateUserWants in AvailableGateLocatorValues:
                AvailableGateLocatorValues.remove(gateUserWants)
                ChosenGateLocatorValues.append(gateUserWants)
            if gateUserWants == 10:
                if len(ChosenGateLocatorValues) == 0:
                    print("You have to select atleast one gate")
                else:
                    print("")
                    return ChosenGateLocatorValues
                
    def GetGateNameCLI():
        name = input("Enter Name for the logic that you are Creating: ")
        return name




NewGateMaker = TruthTableToGatesCLI

#----------------------------Program starts here

TruthTable, inputmask = GatesToTruthTableCLI.main()

inputgatemask = TruthTableToGatesCLI.GateTypeSelectorCLI()

name = TruthTableToGatesCLI.GetGateNameCLI()

start_time = time.time()
#Enter Program here

print(NewGateMaker.logicMaskMaker(inputmask, inputgatemask, TruthTable, name))

#logicMaskValidatorValidator()

print("--- %s seconds ---" % (time.time() - start_time))










def DifferenceinTimeTester():
    start_time = time.time()

    for i in range(0,1000000):
        GatesClass.TWOBITADDER([0,1],[1,0],1)

    print("--- %s seconds ---" % (time.time() - start_time))

#----------

    start_time = time.time()

    for i in range(0,1000000):
        GatesClass.TWOBITADDERFORMYSELF(0,1,1,0,1)

    print("--- %s seconds ---" % (time.time() - start_time))


def logicMaskValidatorValidator():
    """Helps test the logicMaskValidator inorder to make shure it actually works"""
    NewGateMaker = TruthTableToGatesCLI

    exampleLogicMask1 = ["ADDER",[["X1","bool"], ["X2","bool"], ["X3","bool"]],[["Y1",[7,[[7,["X1","X2"]],"X3"]]],["Y2",[4,[[3,[[7,["X1","X2"]],"X3"]],[3,["X2","X1"]]]]]]]
    ExampleTruthTable1 = [[[[0], [0], [0]], [[1], [0], [0]], [[0], [1], [0]], [[1], [1], [0]], [[0], [0], [1]], [[1], [0], [1]], [[0], [1], [1]], [[1], [1], [1]]], [[[0, 0]], [[1, 0]], [[1, 0]], [[0, 1]], [[1, 0]], [[0, 1]], [[0, 1]], [[1, 1]]]]
    output1 = NewGateMaker.logicMaskValidator(exampleLogicMask1, ExampleTruthTable1)

    if output1 == 1:
        print("We had a winner!")
    else:
        print("we did not have a winner!")


    exampleLogicMask2 = ["sevensegdisplaydriver",[["X1","list"]],[["Y1", [0,["X4"]]],["Y2", [4,[[7,[[7,["X4","X3"]],[5,["X4",[4,["X2","X1"]]]]]],[4,[[3,[[4,[[7,["X3","X2"]],[1,["X1"]]]],"X1"]],[5,[[5,[[1,["X3"]],"X2"]],"X1"]]]]]]],["Y3", [6,[[3,[[7,["X4","X3"]],[4,["X2","X1"]]]],[4,["X2","X1"]]]]],["Y4", [4,[[6,[[6,[[3,[[7,["X4","X3"]],[4,["X2","X1"]]]],[4,["X2","X1"]]]],[4,["X2","X1"]]]],"X1"]]],["Y5", [4,[[3,[[4,[[7,["X3","X2"]],[1,["X1"]]]],"X1"]],[5,[[5,[[1,["X3"]],"X2"]],"X1"]]]]],["Y6", [5,[[5,[[1,["X3"]],"X2"]],"X1"]]],["Y7", [6,[[6,[[3,[[7,["X4","X3"]],[4,["X2","X1"]]]],[4,["X2","X1"]]]],[4,["X2","X1"]]]],"X1"],["Y8", [4,[[7,[[5,["X4",[4,["X2","X1"]]]],[4,[[7,["X3","X2"]],[1,["X1"]]]]]],[5,[[1,["X3"]],"X2"]]]]]]]
    ExampleTruthTable2 = [[[[0, 0, 0, 0]], [[1, 0, 0, 0]], [[0, 1, 0, 0]], [[1, 1, 0, 0]], [[0, 0, 1, 0]], [[1, 0, 1, 0]], [[0, 1, 1, 0]], [[1, 1, 1, 0]], [[0, 0, 0, 1]], [[1, 0, 0, 1]], [[0, 1, 0, 1]], [[1, 1, 0, 1]], [[0, 0, 1, 1]], [[1, 0, 1, 1]], [[0, 1, 1, 1]], [[1, 1, 1, 1]]], [[[0, 1, 1, 1, 1, 1, 1, 0]], [[0, 0, 1, 1, 0, 0, 0, 0]], [[0, 1, 1, 0, 1, 1, 0, 1]], [[0, 1, 1, 1, 1, 0, 0, 1]], [[0, 0, 1, 1, 0, 0, 1, 1]], [[0, 1, 0, 1, 1, 0, 1, 1]], [[0, 1, 0, 1, 1, 1, 1, 1]], [[0, 1, 0, 1, 0, 0, 1, 0]], [[1, 1, 1, 1, 1, 1, 1, 1]], [[1, 1, 0, 1, 0, 0, 1, 0]], [[1, 1, 0, 1, 1, 1, 1, 1]], [[1, 1, 0, 1, 1, 0, 1, 1]], [[1, 0, 1, 1, 0, 0, 1, 1]], [[1, 1, 1, 1, 1, 0, 0, 1]], [[1, 1, 1, 0, 1, 1, 0, 1]], [[1, 0, 1, 1, 0, 0, 0, 0]]]]
    output2 = NewGateMaker.logicMaskValidator(exampleLogicMask2, ExampleTruthTable2)

    if output2 == 1:
        print("We had a winner!")
    else:
        print("we did not have a winner!")


    for i in range(1, 2):
    
        exampleLogicMask3 = ["TwoBitAdder",[["X1","list"],["X2","list"],["X3","bool"]],[["Y1", [7,[[7,["X1","X3"]],"X5"]]],["Y2", [7,[[7,["X2","X4"]],[4,[[3,[[7,["X1","X3"]],"X5"]],[3,["X1","X3"]]]]]]],["Y3", [4,[[3,[[7,["X2","X4"]],[4,[[3,[[7,["X1","X3"]],"X5"]],[3,["X1","X3"]]]]]],[3,["X2","X4"]]]]]]]
        ExampleTruthTable3 = [[[[0], [0], [0], [0], [0]], [[1], [0], [0], [0], [0]], [[0], [1], [0], [0], [0]], [[1], [1], [0], [0], [0]], [[0], [0], [1], [0], [0]], [[1], [0], [1], [0], [0]], [[0], [1], [1], [0], [0]], [[1], [1], [1], [0], [0]], [[0], [0], [0], [1], [0]], [[1], [0], [0], [1], [0]], [[0], [1], [0], [1], [0]], [[1], [1], [0], [1], [0]], [[0], [0], [1], [1], [0]], [[1], [0], [1], [1], [0]], [[0], [1], [1], [1], [0]], [[1], [1], [1], [1], [0]], [[0], [0], [0], [0], [1]], [[1], [0], [0], [0], [1]], [[0], [1], [0], [0], [1]], [[1], [1], [0], [0], [1]], [[0], [0], [1], [0], [1]], [[1], [0], [1], [0], [1]], [[0], [1], [1], [0], [1]], [[1], [1], [1], [0], [1]], [[0], [0], [0], [1], [1]], [[1], [0], [0], [1], [1]], [[0], [1], [0], [1], [1]], [[1], [1], [0], [1], [1]], [[0], [0], [1], [1], [1]], [[1], [0], [1], [1], [1]], [[0], [1], [1], [1], [1]], [[1], [1], [1], [1], [1]]], [[[0, 0, 0]], [[1, 0, 0]], [[0, 1, 0]], [[1, 1, 0]], [[1, 0, 0]], [[0, 1, 0]], [[1, 1, 0]], [[0, 0, 1]], [[0, 1, 0]], [[1, 1, 0]], [[0, 0, 1]], [[1, 0, 1]], [[1, 1, 0]], [[0, 0, 1]], [[1, 0, 1]], [[0, 1, 1]], [[1, 0, 0]], [[0, 1, 0]], [[1, 1, 0]], [[0, 0, 1]], [[0, 1, 0]], [[1, 1, 0]], [[0, 0, 1]], [[1, 0, 1]], [[1, 1, 0]], [[0, 0, 1]], [[1, 0, 1]], [[0, 1, 1]], [[0, 0, 1]], [[1, 0, 1]], [[0, 1, 1]], [[1, 1, 1]]]]
        output3 = NewGateMaker.logicMaskValidator(exampleLogicMask3, ExampleTruthTable3)

    if output3 == 1:
        print("We had a winner!")
    else:
        print("we did not have a winner!")


    """exampleLogicMask3 = ["TwoBitAdder",[["X1","list"],["X2","list"],["X3","bool"]],[["Y1", [7,[[7,["X1","X3"]],"X5"]]],["Y2", [7,[[7,["X2","X4"]],[4,[[3,[[7,["X1","X3"]],"X5"]],[3,["X1","X3"]]]]]]],["Y3", [4,[[3,[[7,["X2","X4"]],[4,[[3,[[7,["X1","X3"]],"X5"]],[3,["X1","X3"]]]]]],[3,["X2","X4"]]]]]]]
    ExampleTruthTable3 = [[[[0], [1], [1], [0], [0]]], [[[1, 1, 0]]]]
    output3 = NewGateMaker.logicMaskValidator(exampleLogicMask3, ExampleTruthTable3)

    if output3 == 1:
        print("We had a winner!")
    else:
        print("we did not have a winner!")"""
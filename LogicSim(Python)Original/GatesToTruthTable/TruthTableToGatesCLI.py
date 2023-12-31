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
    
    def logicMaskMaker(inputmask:list, inputgatemask:list, TruthTable:list, depthmask:list, name:str="UserCreatedGate", timelimit:int=99999999999999):
        """Takes in a input mask ([[[0],[0],[0]],[[0],[0]]]) and creates the logic mask ([Y2, [Logic]]) based on a the inputGateMask, and depth mask
            the depth mask is just a way for the program to know the range of depth its allowed to search up to for each function, [Y1, []].
            If i do one input at a time and stop searching for that input when it finds the correct var, it should be MUCH quicker than if i dont.
        """
        HardlogicMask = ["ADDER",[["X1","bool"], ["X2","bool"], ["X3","bool"]],[["Y1",[7,[[7,["X1","X2"]],"X3"]]],["Y2",[4,[[3,[[7,["X1","X2"]],"X3"]],[3,["X2","X1"]]]]]]]
        
        logicMask = [name,[],[]]

        justinputsfromIOmask = inputmask[0]
        justoutputsfromIOmask = inputmask[1]

        inputnum = 1
        for inputRAW in justinputsfromIOmask:
            if len(inputRAW) > 1:
                logicMask[1].append([f"X{inputnum}","list"])
            else:
                logicMask[1].append([f"X{inputnum}","bool"])
            inputnum += 1

        inputvars = []

        for input in range(0, len(logicMask[1])):
            inputvars.append(logicMask[1][input][0])


        outputnum = 1
        for outputRAW in justoutputsfromIOmask:
            logicMask[2].append([f"Y{outputnum}",[]])
            outputnum += 1    

        

        logicMasks = []
        print(f"Starting mask = {logicMask}")
        maskResults = 0

        while True:
            #code goes here
            for output in range(0, len(justoutputsfromIOmask)):
                internalTimeTaken = time.time()
                workingmasks = []
                #print("Masks reset")

                maskResults, workingmask = TruthTableToGatesCLI.generate_combinations(depthmask[1], inputgatemask, inputvars, TruthTable, internalTimeTaken, workingmasks, logicMask, output)

                if output != len(justoutputsfromIOmask):

                    if maskResults == "Continue Thinking" and workingmask != None:
                        workingmasks.append(workingmask)

                    elif maskResults == "End of the line buddy" and workingmask != None:
                        workingmasks.append(workingmask)
                        logicMask[2][output][1] = workingmask[0]
                    
            else:
                something = str(logicMask)
                logicMasks.append(utilsV1.convert_string_to_list(something))
                finalresult = f"Final results:\n"
                for logicmassk in logicMasks:
                    finalresult += f"{logicmassk}\n"
                return finalresult
        #code ends here

    def generate_combinations(depth:int, gates:list, variables:list, TruthTable:list, internalTimeTaken:float,  workingmasks:list, logicMask:list, outputnum:int):

        
        logicMask3 = str(logicMask)
        logicMask2 = utilsV1.convert_string_to_list(logicMask3)
        
        if depth == 0:
            
            for gate in gates:
                if gate == 0 or gate == 1:
                    for variable1 in variables:

                        Newbornmask = [gate, [variable1]]
                        logicMask2[2][outputnum][1] = Newbornmask
                        #print(f"{gate} - {variable1}        {Newbornmask}              {logicMask2[2][outputnum]}")
                        newbornmaskresults = TruthTableToGatesCLI.logicMaskValidator(logicMask2, TruthTable, outputnum + 1)


                        #Probbly can be turned into a function:

                        #test if newborn mask has allready been found
                        if newbornmaskresults == 1:

                            if Newbornmask in workingmasks:
                                pass
                            else:
                                #Doesnt actually work
                                #Determing if the gate is too large to nicely fit on the screen
                                if True == True:
                                    #print(f"Found one! It looked like:\n{logicMask2}\n")
                                    pass

                                #Gets user input to see if they want to search for more valid answers
                                #contineTheSearch = utilsV1.get_int("Do you want to continue searching for more valid answers? (1 = yes, 0 = no): ")
                                contineTheSearch = 0

                                if contineTheSearch == 0:
                                    return "End of the line buddy", Newbornmask
                                if contineTheSearch == 1:
                                    return "Continue Thinking", Newbornmask

                        internalTimeTaken = TruthTableToGatesCLI.timetostop(internalTimeTaken)

                        if internalTimeTaken == True:
                            return "End of the line buddy", None

                        #i attempted to make it into a function
                        #return TruthTableToGatesCLI.combotester(newbornmaskresults, Newbornmask, workingmasks, logicMask2, internalTimeTaken)
     
                else:    
                    for variable1 in variables:
                        for variable2 in variables:
        
                            Newbornmask = [gate, [variable1,variable2]]
                            logicMask2[2][outputnum][1] = Newbornmask
                            #print(f"{gate} - {variable1}        {Newbornmask}              {logicMask2[2][outputnum]}")
                            newbornmaskresults = TruthTableToGatesCLI.logicMaskValidator(logicMask2, TruthTable, outputnum + 1)


                            #Probbly can be turned into a function:

                            #test if newborn mask has allready been found
                            if newbornmaskresults == 1:

                                if Newbornmask in workingmasks:
                                    pass
                                else:
                                    #Doesnt actually work
                                    #Determing if the gate is too large to nicely fit on the screen
                                    if True == True:
                                        #print(f"Found one! It looked like:\n{logicMask2}\n")
                                        pass

                                    #Gets user input to see if they want to search for more valid answers
                                    #contineTheSearch = utilsV1.get_int("Do you want to continue searching for more valid answers? (1 = yes, 0 = no): ")
                                    contineTheSearch = 0

                                    if contineTheSearch == 0:
                                        return "End of the line buddy", Newbornmask
                                    if contineTheSearch == 1:
                                        return "Continue Thinking", Newbornmask

                            internalTimeTaken = TruthTableToGatesCLI.timetostop(internalTimeTaken)

                            if internalTimeTaken == True:
                                return "End of the line buddy", None

                            #i attempted to make it into a function
                            #return TruthTableToGatesCLI.combotester(newbornmaskresults, Newbornmask, workingmasks, logicMask2, internalTimeTaken)
                            
        if depth > 0:
            #Makes every combination before the last one
            combinations = []
            for gate in gates:
                if gate == 0 or gate == 1:
                    for variable1 in variables:
                        Newbornmask = [[gate, [variable1]]]
                        combinations.extend(Newbornmask)
                        #print(Newbornmask)

                        #I think this is logic that will short circuit the program
                        logicMask2[2][outputnum][1] = Newbornmask[0]
                        newbornmaskresults = TruthTableToGatesCLI.logicMaskValidator(logicMask2, TruthTable, outputnum + 1)
                        #Probbly can be turned into a function:

                        #test if newborn mask has allready been found
                        if newbornmaskresults == 1:

                            if Newbornmask in workingmasks:
                                pass
                            else:
                                #Doesnt actually work
                                #Determing if the gate is too large to nicely fit on the screen
                                if True == True:
                                    #print(f"Found one! It looked like:\n{logicMask2}\n")
                                    pass

                                #Gets user input to see if they want to search for more valid answers
                                #contineTheSearch = utilsV1.get_int("Do you want to continue searching for more valid answers? (1 = yes, 0 = no): ")
                                contineTheSearch = 0

                                if contineTheSearch == 0:
                                    return "End of the line buddy", Newbornmask
                                if contineTheSearch == 1:
                                    return "Continue Thinking", Newbornmask

                        internalTimeTaken = TruthTableToGatesCLI.timetostop(internalTimeTaken)

                        if internalTimeTaken == True:
                            return "End of the line buddy", None

                        #i attempted to make it into a function
                        #return TruthTableToGatesCLI.combotester(newbornmaskresults, Newbornmask, workingmasks, logicMask2, internalTimeTaken)
                        
                else:
                    for variable1 in variables:
                        for variable2 in variables:
                            Newbornmask = [[gate, [variable1,variable2]]]
                            combinations.extend(Newbornmask)
                            #print([gate, [variable1,variable2]])

                            #I think this is logic that will short circuit the program
                            logicMask2[2][outputnum][1] = Newbornmask[0]
                            newbornmaskresults = TruthTableToGatesCLI.logicMaskValidator(logicMask2, TruthTable, outputnum + 1)

                            #Probbly can be turned into a function:

                            #test if newborn mask has allready been found
                            if newbornmaskresults == 1:

                                if Newbornmask in workingmasks:
                                    pass
                                else:
                                    #Doesnt actually work
                                    #Determing if the gate is too large to nicely fit on the screen
                                    if True == True:
                                        #print(f"Found one! It looked like:\n{logicMask2}\n")
                                        pass


                                    #Gets user input to see if they want to search for more valid answers
                                    #contineTheSearch = utilsV1.get_int("Do you want to continue searching for more valid answers? (1 = yes, 0 = no): ")
                                    contineTheSearch = 0

                                    if contineTheSearch == 0:
                                        return "End of the line buddy", Newbornmask
                                    if contineTheSearch == 1:
                                        return "Continue Thinking", Newbornmask

                            internalTimeTaken = TruthTableToGatesCLI.timetostop(internalTimeTaken)

                            if internalTimeTaken == True:
                                return "End of the line buddy", None

                            #i attempted to make it into a function
                            #return TruthTableToGatesCLI.combotester(newbornmaskresults, Newbornmask, workingmasks, logicMask2, internalTimeTaken)

            depth -= 1
            return TruthTableToGatesCLI.generate_combinations(depth, gates, combinations, TruthTable, internalTimeTaken, workingmasks, logicMask, outputnum)
        return "End of the line buddy", None

    def timetostop(internalTimeTaken, whentostop:int=10):
        #stop the code after a desegnated about of time
        if time.time() - internalTimeTaken > whentostop:
            contineTheSearch = utilsV1.get_int("\nNothing has happend in a while... want to continue searching? (1 = yes, 0 = no): ")
            if contineTheSearch == 0:

                return True
        return time.time()

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

                    gateinputs = utilsV1.variableUnifier(TruthTable[0][truthtablelen])

                    currentanswer = TruthTableToGatesCLI.outputLogicator(currentlist[1], gateinputs)

                    currentlogicOut[0].append(currentanswer)

                logicOut.append(currentlogicOut)

                currentTruthTableUnified = utilsV1.variableUnifier(TruthTable[1][truthtablelen][0])

                if currentlogicOut == [[currentTruthTableUnified[TestThisInput-1]]]:
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

                gateinputs = utilsV1.variableUnifier(TruthTable[0][truthtablelen])

                #print("-"*30)
                #print(f"current list{currentlist[1]}\nGate inputs{gateinputs}\n")
                currentanswer = TruthTableToGatesCLI.outputLogicator(currentlist[1], gateinputs)

                currentlogicOut[0].append(currentanswer)

            #print("-"*30)
            logicOut.append(currentlogicOut)

            #short circuts the function if it finds something that doesnt work
            currentTruthTableUnified = [utilsV1.variableUnifier(TruthTable[1][truthtablelen][0])]

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
        #print(logicIn)
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

depth = [0, utilsV1.get_int("Enter Depth for which the computer should search: ")]

timeLimit = utilsV1.get_int("Enter the Time limit in secconds: +")

start_time = time.time()
#Enter Program here


"""#------------------
inputmask = [[[0],[0]],[[0]]]
inputgatemask = [3]
TruthTable = [[[[0], [0]], [[1], [0]], [[0], [1]], [[1], [1]]], [[[0]], [[0]], [[0]], [[1]]]]
name = "AND"
depth = [0,0]
#------------------

answer = NewGateMaker.logicMaskMaker(inputmask, inputgatemask, TruthTable, depth, name)
print(answer)

#------------------
inputmask = [[[0],[0],[0]],[[0],[0]]]
inputgatemask = [0,6,7]
TruthTable = [[[[0], [0], [0]], [[1], [0], [0]], [[0], [1], [0]], [[1], [1], [0]], [[0], [0], [1]], [[1], [0], [1]], [[0], [1], [1]], [[1], [1], [1]]], [[[0, 0]], [[1, 0]], [[1, 0]], [[0, 1]], [[1, 0]], [[0, 1]], [[0, 1]], [[1, 1]]]]
name = "ADDER"
depth = [0,2]
#------------------

answer = NewGateMaker.logicMaskMaker(inputmask, inputgatemask, TruthTable, depth, name)
print(answer)

#------------------
inputmask = [[[0],[0],[0],[0],[0]],[[0],[0],[0]]]
inputgatemask = [0,1,3,4,5,6,7]
TruthTable = [[[[0, 0], [0, 0], [0]], [[1, 0], [0, 0], [0]], [[0, 1], [0, 0], [0]], [[1, 1], [0, 0], [0]], [[0, 0], [1, 0], [0]], [[1, 0], [1, 0], [0]], [[0, 1], [1, 0], [0]], [[1, 1], [1, 0], [0]], [[0, 0], [0, 1], [0]], [[1, 0], [0, 1], [0]], [[0, 1], [0, 1], [0]], [[1, 1], [0, 1], [0]], [[0, 0], [1, 1], [0]], [[1, 0], [1, 1], [0]], [[0, 1], [1, 1], [0]], [[1, 1], [1, 1], [0]], [[0, 0], [0, 0], [1]], [[1, 0], [0, 0], [1]], [[0, 1], [0, 0], [1]], [[1, 1], [0, 0], [1]], [[0, 0], [1, 0], [1]], [[1, 0], [1, 0], [1]], [[0, 1], [1, 0], [1]], [[1, 1], [1, 0], [1]], [[0, 0], [0, 1], [1]], [[1, 0], [0, 1], [1]], [[0, 1], [0, 1], [1]], [[1, 1], [0, 1], [1]], [[0, 0], [1, 1], [1]], [[1, 0], [1, 1], [1]], [[0, 1], [1, 1], [1]], [[1, 1], [1, 1], [1]]], [[[[0, 0], 0]], [[[1, 0], 0]], [[[0, 1], 0]], [[[1, 1], 0]], [[[1, 0], 0]], [[[0, 0], 1]], [[[1, 1], 0]], [[[0, 1], 1]], [[[0, 1], 0]], [[[1, 1], 0]], [[[1, 0], 0]], [[[0, 0], 1]], [[[1, 1], 0]], [[[0, 1], 1]], [[[0, 0], 1]], [[[1, 0], 1]], [[[0, 1], 0]], [[[1, 1], 0]], [[[1, 0], 0]], [[[0, 0], 1]], [[[1, 1], 0]], [[[0, 1], 1]], [[[0, 0], 1]], [[[1, 0], 1]], [[[1, 0], 0]], [[[0, 0], 1]], [[[1, 1], 0]], [[[0, 1], 1]], [[[0, 0], 1]], [[[1, 0], 1]], [[[0, 1], 1]], [[[1, 1], 1]]]]
name = "2ADDER"
depth = [0,3]
timeLimit = 99999999999999
#------------------
"""
answer = NewGateMaker.logicMaskMaker(inputmask, inputgatemask, TruthTable, depth, name, timeLimit)
print(answer)

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
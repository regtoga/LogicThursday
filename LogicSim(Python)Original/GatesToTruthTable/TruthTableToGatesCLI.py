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

import GatesClass
import GataDataFunctions


class TruthTableToGatesCLI():
    def __init__(self) -> None:
        pass

    def potentialGatepacker(truthTable:list, inputOutputMask:list, GateMask:list) -> list:
        """Potential gate = 
        [ADDER,[[[X1,#]], [[X2,#]], [[X3,#]]],[[[Y1,[7,[[7,[X1,X2]],X3]]]],[[Y2, [Y2, [4,[[3,[[7,[X1,X2]],X3]],[3,[X2,X1]]]]]]]]]
        or
        [
            ADDER, 
            [
                [
                    [X1, #]
                ], 
                [
                    [X2, #]
                ], 
                [
                    [X3, #]
                ]
            ],
            [
                [
                    [Y1,[7,[[7,[X1,X2]],X3]]] #SUM
                ], 
                [
                    [Y2, [4,[[3,[[7,[X1,X2]],X3]],[3,[X2,X1]]]]] #Carry Out
                ]
            ]
        ]

        input/output mask: [[[0],[0],[0]],[[0],[0]]]
        Truthtable:        [[0], [1], [1]], [[1], [1], [1]]], [[(0, 0)], [(1, 0)], [(1, 0)], [(0, 1)], [(1, 0)], [(0, 1)], [(0, 1)], [(1, 1)]]]
        GateMask:          [3, 4, 7]
        """

        truthTable = [[[[0], [1], [1]], [[1], [1], [1]]], [[(0, 0)], [(1, 0)], [(1, 0)], [(0, 1)], [(1, 0)], [(0, 1)], [(0, 1)], [(1, 1)]]]
        inputOutputMask = [[[0],[0],[0]],[[0],[0]]]
        GateMask = [3, 4, 7]

        HardPotentialGate = ["ADDER",[["X1","bool"], ["X2","bool"], ["X3","bool"]],[[["Y1",[7,[[7,["X1","X2"]],"X3"]]]],[["Y2", [4,[[3,[[7,["X1","X2"]],"X3"]],[3,["X2","X1"]]]]]]]]
        PotentialGate = []
        print(f"{truthTable}\n{inputOutputMask}\n{GateMask}")



        return PotentialGate
    
    def logicMaskMaker(inputmask:list, inputgamemask:list, inputnum:int, seed:int):
        """Takes in a input mask ([[[0],[0],[0]],[[0],[0]]]) and creates the logic mask ([Y2, [Logic]]) based on a the inputGateMask, inputnum, and a seed"""
        print()

    #----------------------------------- function should try all combinations of the program and compare the ouput with the truth table
    def logicMaskValidator(logicMask:list="", TruthTable:list="") -> bool:
        """gate format [name, [inputs], [outputs, [Logic]]]
        returns true or false depending on if the logic mask actually fufills the desired outcome"""
        
        if logicMask[0] == "" or TruthTable[0] == "":
            return False

        logicOut = []

        name = logicMask[0]
        inputs = logicMask[1]
        outputsANDlogic = logicMask[2]
        print(f"{name}, \n{inputs}, \n{outputsANDlogic}")
        print("---")
        print(f"TruthTableInputs: {TruthTable[0]}")
        print("---")

        #this loops for every different input inside ofe the truthTable inputs side
        
        for truthtablelen in range(0, len(TruthTable[0])):
            print(f"TruthTableInput number: {truthtablelen}.")

            #This portion of the code needs to take the outputsandlogic into consideration and actually execute the code
            #EX mask [['Y1', [7, [[7, ['X1', 'X2']], 'X3']]], ['Y2', [4, [[3, [[7, ['X1', 'X2']], 'X3']], [3, ['X2', 'X1']]]]]]
            numberoutputs = len(outputsANDlogic)

            print(f"num outputs = {numberoutputs}")

            
            currentlogicOut = [[]]
            for outputletters in outputsANDlogic:
                
                currentlist = outputletters
                print(currentlist)
                currentanswer = TruthTableToGatesCLI.outputLogicator(currentlist[1], TruthTable[0][truthtablelen])
                print(f"{currentlist} ='ed {currentanswer}")
                currentlogicOut[0].append(currentanswer)
            print("")

            logicOut.append(currentlogicOut)

            print(f"{currentlogicOut} and the correct answer was > {TruthTable[1][truthtablelen]}")

            if currentlogicOut == TruthTable[1][truthtablelen]:
                print(f"We had a winner!")
                continue
            else:
                return 0

        if logicOut == TruthTable[1]:
            print(f"CORRECT LOGIC MASK!")
            return 1
        else:
            return 0


    def outputLogicator(logicIn:list, variablesIn:list):
        #make a function that takes something that looks like this as input:
        # [7, [7, ['X1', 'X2']], 'X3'] or:
        # [4, [[3, [[7, ['X1', 'X2']], 'X3']], [3, ['X2', 'X1']]]]
        # and outputs the result
        answer = "nothing"
        opperation = logicIn[0]

        data = []

        for logic in logicIn[1]:
            data.append(logic)

        #data2 = logicIn[1]
        print("")
 
        #IMPORTANT doesnt support lists yet! maby?
        if type(data[0]) == str:
            X1 = int(data[0].replace("X",""))
            X1 = variablesIn[X1-1][0] #may have to take the 0 off the end 
            data[0] = X1
        else:
            print(f"opperation: {opperation}")
            print(f"data: {data}")
            if type(opperation) == int:
                intodata1 = TruthTableToGatesCLI.outputLogicator(data[0], variablesIn)
                data[0] = intodata1
        X1 = data[0]

        if len(data) == 2 and type(data[1]) == str:
            X2 = int(data[1].replace("X",""))
            X2 = variablesIn[X2-1][0] #may have to take the 0 off the end 
            data[1] = X2
        else:
            print(f"opperation: {opperation}")
            print(f"data: {data}")
            if type(opperation) == int:
                intodata2 = TruthTableToGatesCLI.outputLogicator(data[1], variablesIn)
                data[1] = intodata2
        X2 = data[1]

        answer = GataDataFunctions.GatesAvailable(opperation,X1,X2)

        return answer


NewGateMaker = TruthTableToGatesCLI

exampleLogicMask1 = ["ADDER",[["X1","bool"], ["X2","bool"], ["X3","bool"]],[["Y1",[7,[[7,["X1","X2"]],"X3"]]],["Y2",[4,[[3,[[7,["X1","X2"]],"X3"]],[3,["X2","X1"]]]]]]]
ExampleTruthTable1 = [[[[0], [0], [0]], [[1], [0], [0]], [[0], [1], [0]], [[1], [1], [0]], [[0], [0], [1]], [[1], [0], [1]], [[0], [1], [1]], [[1], [1], [1]]], [[[0, 0]], [[1, 0]], [[1, 0]], [[0, 1]], [[1, 0]], [[0, 1]], [[0, 1]], [[1, 1]]]]
NewGateMaker.logicMaskValidator(exampleLogicMask1, ExampleTruthTable1)

#NewGateMaker.outputLogicator([2,[[2,["X1","X2"]],"X3"]],[1,1,1])

#["Y1",[7,[[7,["X1","X2"]],"X3"]]]
#["Y2",[4,[[3,[[7,["X1","X2"]],"X3"]],[3,["X2","X1"]]]]]

#This File should ONLY be the CLI the rest goes inside of the TruthTableToGates object

import TruthTableToGatesThinker as Thinker

"""
    1. Ask if user has a preformatted TruthTable if so let them enter it in one line, else continue though steps 2-4
        -preformatted TruthTable: F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7) or F(A,B,C) = Z'M(2,3,4,5)+Z'd(6,7).

    2. Get Ammount of input variables from user -(optional, can compute based of of 3,4 but computer guess may be smaller than user desires).
    3. Get MinTerms from user in [0,1,2,4,6] format, Also Ask If we are computing for Maxterms instead.
    4. Get Dont Cares from userin [8,9,10] format -(optional, arnt required).

    5. Return User Result in "f = CD + A'B'C' + ABD + ABC" format, allow them to save it to a text file or something similar.

    6.Do it again!
"""

#test cases
TtoG = Thinker.TruthTableToGates("F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7)") 
print("\nTestCase 1: ")
print(f"TruthTable      : {TtoG.get_TruthTable()}")
print(f"Number of Inputs: {TtoG.get_NumInputVars()}")
print(f"Min or Max      : {TtoG.get_MinorMax()}")
print(f"minterms        : {TtoG.get_Minterms()}")
print(f"Maxterms        : {TtoG.get_Maxterms()}")
print(f"Dont Cares      : {TtoG.get_DontCares()}")
print(f"{TtoG.get_Answer()}")
print(f"Reformatted TruthTable String: {TtoG.TruthTableDataIntoTruthTable()}")

input("press Enter: ")
print("\nTestCase 2: ")
TtoG2 = Thinker.TruthTableToGates("F() = Z'M(0,1,3,5)+Z'd(2)") 

print(f"TruthTable      : {TtoG2.get_TruthTable()}")
print(f"Number of Inputs: {TtoG2.get_NumInputVars()}")
print(f"Min or Max      : {TtoG2.get_MinorMax()}")
print(f"minterms        : {TtoG2.get_Minterms()}")
print(f"Maxterms        : {TtoG2.get_Maxterms()}")
print(f"Dont Cares      : {TtoG2.get_DontCares()}")
print(f"{TtoG2.get_Answer()}")
print(f"Reformatted TruthTable String: {TtoG2.TruthTableDataIntoTruthTable()}")

input("press Enter: ")
print("\nTestCase 3: ")
TtoG3 = Thinker.TruthTableToGates("F(A,B,C) = Z'M(1)+Z'd(6,7,100)") 

print(f"TruthTable      : {TtoG3.get_TruthTable()}")
print(f"Number of Inputs: {TtoG3.get_NumInputVars()}")
print(f"Min or Max      : {TtoG3.get_MinorMax()}")
print(f"minterms        : {TtoG3.get_Minterms()}")
print(f"Maxterms        : {TtoG3.get_Maxterms()}")
print(f"Dont Cares      : {TtoG3.get_DontCares()}")
print(f"{TtoG3.get_Answer()}")
print(f"Reformatted TruthTable String: {TtoG3.TruthTableDataIntoTruthTable()}")

input("press Enter: ")
print("\nTestCase 4: ")
TtoG4 = Thinker.TruthTableToGates("F(A,B,C,D,E) = Z'm(1,23,101)") 

print(f"TruthTable      : {TtoG4.get_TruthTable()}")
print(f"Number of Inputs: {TtoG4.get_NumInputVars()}")
print(f"Min or Max      : {TtoG4.get_MinorMax()}")
print(f"minterms        : {TtoG4.get_Minterms()}")
print(f"Maxterms        : {TtoG4.get_Maxterms()}")
print(f"Dont Cares      : {TtoG4.get_DontCares()}")
print(f"{TtoG4.get_Answer()}")
print(f"Reformatted TruthTable String: {TtoG4.TruthTableDataIntoTruthTable()}")

input("press Enter: ")
print("\nTestCase 5: ")
TtoG5 = Thinker.TruthTableToGates("Z'm(7)") 

print(f"TruthTable      : {TtoG5.get_TruthTable()}")
print(f"Number of Inputs: {TtoG5.get_NumInputVars()}")
print(f"Min or Max      : {TtoG5.get_MinorMax()}")
print(f"minterms        : {TtoG5.get_Minterms()}")
print(f"Maxterms        : {TtoG5.get_Maxterms()}")
print(f"Dont Cares      : {TtoG5.get_DontCares()}")
print(f"{TtoG5.get_Answer()}")
print(f"Reformatted TruthTable String: {TtoG5.TruthTableDataIntoTruthTable()}")
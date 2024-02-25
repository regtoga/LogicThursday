#This File is temporary and will eventually not need to exist

import TruthTableToGatesThinker as Thinker

#test cases
print("Test 1")
TtoG = Thinker.TruthTableToGates("F(A,B,C,D) = Z'm(0,1,3,7,8,9,11,15)") 

print(f"function: {TtoG.TruthTableDataIntoTruthTable()}")
TtoG.calculateanswer()

print(TtoG.print_all_TABLES())

print(f"\nAnswer: {TtoG.get_Answer()}\n\n")

print("Test 2")
TtoG2 = Thinker.TruthTableToGates("Z'm(3,11,15,19,21)","two") 

print(f"function: {TtoG2.TruthTableDataIntoTruthTable()}")
TtoG2.calculateanswer()
print(f"\nAnswer: {TtoG2.get_Answer()}\n\n")

print("Test 3")
TtoG3 = Thinker.TruthTableToGates("Z'm(0,1,2,3,8,9,10,11,12)","three") 

print(f"function: {TtoG3.TruthTableDataIntoTruthTable()}")
TtoG3.calculateanswer()
print(f"\nAnswer: {TtoG3.get_Answer()}")
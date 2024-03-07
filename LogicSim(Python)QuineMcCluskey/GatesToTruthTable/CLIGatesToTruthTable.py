#This File should ONLY be the CLI the rest goes inside of the GatesToTruthTable object
import GatesToTableThinker as Thinker

print("Test 1:")
#input = Z'm(1,2,3,4,5)
GtoT1 = Thinker.TruthTableToGates("F = A'B + AB'")
print(GtoT1.get_TruthTable())
print(GtoT1.get_AnswerFunction())

print("\nTest 2:")
#input = 
GtoT2 = Thinker.TruthTableToGates("")
print(GtoT2.get_TruthTable())
print(GtoT2.get_AnswerFunction())

print("\nTest 3:")
#input = 
GtoT3 = Thinker.TruthTableToGates("")
print(GtoT3.get_TruthTable())
print(GtoT3.get_AnswerFunction())
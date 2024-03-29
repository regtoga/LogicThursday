#This File should ONLY be the CLI the rest goes inside of the GatesToTruthTable object
import GatesToTableThinker as Thinker

print("Test 1:")
#input = Z'm(2,3,4)
GtoT1 = Thinker.TruthTableToGates("F = A'B + AB'C'")
print(GtoT1.get_TruthTable())
print(GtoT1.get_AnswerFunction())

print("\nTest 2:")
#input = Z'm(1,2,3,4,7,9,12)
GtoT2 = Thinker.TruthTableToGates("F = A'B'C + BC'D' + A'CD + B'C'D")
print(GtoT2.get_TruthTable())
print(GtoT2.get_AnswerFunction())

print("\nTest 3:")
#input = Z'm(77,2,1)
GtoT3 = Thinker.TruthTableToGates("F = AB'C'DEF'G + A'B'C'D'E'FG' + A'B'C'D'E'F'G")
print(GtoT3.get_TruthTable())
print(GtoT3.get_AnswerFunction())
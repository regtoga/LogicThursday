import time
#This File should ONLY be the CLI the rest goes inside of the GatesToTruthTable object
import GatesToTableThinker as Thinker

start_time = time.time()

print("Test 1:")
#input = Z'm(2,3,4)
GtoT1 = Thinker.TruthTableToGates("F = A'B + AB'C'")
print(GtoT1.get_TruthTable())
print("Output: ",GtoT1.get_AnswerFunction())

print("\nTest 2:")
#input = Z'm(1,2,3,4,7,9,12)
GtoT2 = Thinker.TruthTableToGates("F = A'B'C + BC'D' + A'CD + B'C'D")
print(GtoT2.get_TruthTable())
print("Output: ",GtoT2.get_AnswerFunction())

print("\nTest 3:")
#input = Z'm(77,2,1)
GtoT3 = Thinker.TruthTableToGates("F = AB'C'DEF'G + A'B'C'D'E'FG' + A'B'C'D'E'F'G")
print(GtoT3.get_TruthTable())
print("Output: ",GtoT3.get_AnswerFunction())

#print("\nTest 4:")
#input = Z'm(1000,10001)
#GtoT4 = Thinker.TruthTableToGates("F = A'B'C'D'E'F'Z")
#print(GtoT4.get_TruthTable())
#print(GtoT4.get_AnswerFunction())

"""print("\nTest 5:")
#input = Z'm(Random Crap)
GtoT5 = Thinker.TruthTableToGates("F = a'")
#print(GtoT5.get_AnswerFunction())
#print(GtoT5.get_TruthTable())"""

end_time = time.time()

print(f"The functions took {end_time - start_time} seconds to run.")
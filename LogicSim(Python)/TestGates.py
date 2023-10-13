import GatesClass as gate
import utilsV1 as util

X4 = util.get_int("Enter 0 or 1: ")
X3 = util.get_int("Enter 0 or 1: ")
X2 = util.get_int("Enter 0 or 1: ")
X1 = util.get_int("Enter 0 or 1: ")
print([X4,X3,X2,X1])

Y4 = util.get_int("Enter 0 or 1: ")
Y3 = util.get_int("Enter 0 or 1: ")
Y2 = util.get_int("Enter 0 or 1: ")
Y1 = util.get_int("Enter 0 or 1: ")
print([Y4,Y3,Y2,Y1])

Subtract = util.get_int("Enter 0 or 1: ")

print(gate.ALU([X4,X3,X2,X1],[Y4,Y3,Y2,Y1],Subtract))
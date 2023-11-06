#A simple file to test the functions of gates until i build a proper one

import GatesClass as gate
import utilsV1 as util

#memory = gate.set_reset_latch()

#for i in range(0,3):
    #set = util.get_int("Enter 0 or 1: ")
    #reset = util.get_int("Enter 0 or 1: ")
    #output = memory.Latch(set,reset)
    #print(f"while set = {set} and reset = {reset}, the output was: {output}")


#memory = gate.data_latch()
#for i in range(0,10):
    #X1 = util.get_int("Enter 0 or 1: ")
    #clock = util.get_int("Enter 0 or 1: ")
    #output = memory.datalatch(X1,clock)
    #print(f"while data = {X1} and clock = {clock}, the output was: {output}")


#latch = gate.DataFlipFlop()
#for i in range(0,10):

    #X1 = util.get_int("Enter 0 or 1: ")
    #clock = util.get_int("Enter 0 or 1: ")
    #output = latch.FlipFlop(X1,clock)
    #print(f"while data = {X1} and clock = {clock}, the output was: {output}")



#register = gate.four_bit_register()

#while True == True:
    #X4 = util.get_int("Enter 0 or 1: ")
    #X3 = util.get_int("Enter 0 or 1: ")
    #X2 = util.get_int("Enter 0 or 1: ")
    #X1 = util.get_int("Enter 0 or 1: ")
    #print(f"input = {[X4, X3, X2, X1]}")

    #store = util.get_int("Enter 0 or 1: ")

    #clock = util.get_int("Enter 0 or 1: ")

    #output = register.four_bit_register([X4, X3, X2, X1],store, clock)
    
    #print(f"output = {output}")



#def testALU():
#X4 = util.get_int("Enter 0 or 1: ")
#X3 = util.get_int("Enter 0 or 1: ")
#X2 = util.get_int("Enter 0 or 1: ")
#X1 = util.get_int("Enter 0 or 1: ")
#print([X4,X3,X2,X1])
#print(f"{[X4,X3,X2,X1]} ='s {util.binary_to_decimal([X4,X3,X2,X1])}")

#Y4 = util.get_int("Enter 0 or 1: ")
#Y3 = util.get_int("Enter 0 or 1: ")
#Y2 = util.get_int("Enter 0 or 1: ")
#Y1 = util.get_int("Enter 0 or 1: ")
#print(f"{[Y4,Y3,Y2,Y1]} ='s {util.binary_to_decimal([Y4,Y3,Y2,Y1])}")

#Subtract = util.get_int("Enter 0 or 1 (key: 0 ='s add || 1 ='s subtract): ")

#ADDERout, carryout, negative, zero = gate.ALU([X4,X3,X2,X1],[Y4,Y3,Y2,Y1],Subtract)

#if Subtract == 0:
#    print(f"{[X4,X3,X2,X1]} + {[Y4,Y3,Y2,Y1]} = {util.binary_to_decimal(ADDERout)}")
#else:
#    print(f"{[X4,X3,X2,X1]} - {[Y4,Y3,Y2,Y1]} = {util.binary_to_decimal(ADDERout)}")


#def testsixtyfourbitadder():

#X = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
#Y = [0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
#Z = 0

#print(f"{X}\n='s\n{util.binary_to_decimal(X)}")
#print("")
#print(f"{Y}\n='s\n{util.binary_to_decimal(Y)}")
#print("")
#ADDERout, carryout = gate.SixtyFourBitADDERSmall(X,Y,Z)

#print(f"{X}\n{Y}\n{ADDERout}")
#print("")
#print(f"{util.binary_to_decimal(X)}\n+\n{util.binary_to_decimal(Y)}\n=\n{util.binary_to_decimal(ADDERout)}")

"""
["Y1", [0,["X4"]]],
["Y2", [4,[[7,[[7,["X4","X3"]],[5,["X4",[4,["X2","X1"]]]]]],[4,[[3,[[4,[[7,["X3","X2"]],[1,["X1"]]]],"X1"]],[5,[[5,[[1,["X3"]],"X2"]],"X1"]]]]]]],
["Y3", [6,[[3,[[7,["X4","X3"]],[4,["X2","X1"]]]],[4,["X2","X1"]]]]],
["Y4", [4,[[6,[[6,[[3,[[7,["X4","X3"]],[4,["X2","X1"]]]],[4,["X2","X1"]]]],[4,["X2","X1"]]]],"X1"]]],
["Y5", [4,[[3,[[4,[[7,["X3","X2"]],[1,["X1"]]]],"X1"]],[5,[[5,[[1,["X3"]],"X2"]],"X1"]]]]],
["Y6", [5,[[5,[[1,["X3"]],"X2"]],"X1"]]],
["Y7", [6,[[6,[[3,[[7,["X4","X3"]],[4,["X2","X1"]]]],[4,["X2","X1"]]]],[4,["X2","X1"]]]],"X1"],
["Y8", [4,[[7,[[5,["X4",[4,["X2","X1"]]]],[4,[[7,["X3","X2"]],[1,["X1"]]]]]],[5,[[1,["X3"]],"X2"]]]]]
"""

exampleLogicMask1 = ["sevensegdisplaydriver",[["X1","list"],["X2","list"],["X3","bool"]],[]]



[0,[""]] #nothing
[1,[""]] #not
[3,["",""]] #AND
[4,["",""]] #OR
[5,["",""]] #NOR
[6,["",""]] #NAND
[7,["",""]] #XOR





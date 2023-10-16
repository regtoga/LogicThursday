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



register = gate.four_bit_register()

while True == True:
    X4 = util.get_int("Enter 0 or 1: ")
    X3 = util.get_int("Enter 0 or 1: ")
    X2 = util.get_int("Enter 0 or 1: ")
    X1 = util.get_int("Enter 0 or 1: ")
    print(f"input = {[X4, X3, X2, X1]}")

    store = util.get_int("Enter 0 or 1: ")

    clock = util.get_int("Enter 0 or 1: ")

    output = register.four_bit_register([X4, X3, X2, X1],store, clock)
    
    print(f"output = {output}")



def testALU():
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
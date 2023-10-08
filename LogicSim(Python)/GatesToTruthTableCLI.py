#Name: GatesToTruthTable.py
#Author: Aidan Newberry
#Created: 10/6/2023
#Purpose: CLI to turn a predefined Gate array into a TruthTable.

import GatesClass as gate
import utilsV1 as utils

def main():

    #print(str(gate.FOURBITADDER(1,1,1,1,0,0,0,1,0)))

    inputTWOx = [1,1]
    inputTWOy = [1,1]

    inputFOURx = [1,0,1,1]
    inputFOURy = [0,1,0,0]

    inputEIGHTx = [0,1,0,1,0,1,0,1]
    inputEIGHTy = [1,0,1,0,1,0,1,1]

    rad1 = utils.binary_to_decimal(inputEIGHTx)
    rad2 = utils.binary_to_decimal(inputEIGHTy)

    additon, carry = gate.EIGHTBITADDERsmall(inputEIGHTx, inputEIGHTy, 0)
    print(f"{additon},{carry}")
    print(f"{rad1}+{rad2}={utils.binary_to_decimal(additon)}")

    #print(gate.EIGHTBITADDERsmall(input1, input2, 0))

    #in the future i want to be able to input into any function an array of bits EX:
    # x = [[0,1]] y = [[0,1], [1,0]] Z = []


    #x = [[0,0,0,0,1,1,1,1],[0,0,1,1,0,0,1,1],[0,1,0,1,0,1,0,1]]
    #y = [[0,1,0,1,0,1,0,1],[0,0,1,1,0,0,0,1]]

    #print(utils.format_truth_table(x, y))



if __name__ == "__main__":
    main()

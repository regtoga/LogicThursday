"""
    Name: utilsV1.py
    Author: Aidan Newberry
    Created: 10/3/2023
    Purpose: A utility module with commonly used functions
"""

def get_title(program_title):
    """
        Takes in a string argument
        returns a string with ascii decorations
    """
    #Get the length of the statement
    text_length = len(program_title)

    #Create the title string by concatenation

    title_string = "+--" + "-" * text_length + "--+\n"
    title_string = title_string + "|  " + program_title + "  |\n"
    title_string = title_string + "+--" + "-" * text_length + "--+\n"

    #Return the concatenated title string
    return title_string


def get_float(prompt):
    """
        Get a float from the user with try catch
        The prompt string parameter is used to ask the user 
        for the type of input needed
    """
    #Declare local variable
    num = 0

    #Ask the user for an input based on the what parameter
    num = input(prompt)

    #If the input is numeric, convert to float and return
    try:
        return float(num)
    
    #if the input is not numberic, 
    #inform the user and ask for input again
    except ValueError:
        print(f'You entered; {num}, which is not a number.')
        print(f"Let's try that again.\n")

        #Call function from the beginning
        #this is a recursive function call
        return get_float(prompt)

def binary_to_decimal(Xbools: list) -> int:
    """Takes an input of binary and converts it into decimal"""
    exponent = len(Xbools)-1

    decimalnumber = 0

    #used the simplest and most common way to convert a binary number into decimal, def doesnt work with decimals
    for i in range(0, (len(Xbools))):  
        
        if Xbools[i] == 1:
            decimalnumber += 2**exponent
        
        exponent = exponent - 1
    #print(decimalnumber)
    return decimalnumber
        
def fourBitList_into_individual_bools(Xbools: list) -> bool:
    """Takes a list 4 long and sepperates it into 4 seperate variables"""
    X1 = Xbools[0]
    X2 = Xbools[1]
    X3 = Xbools[2]
    X4 = Xbools[3]
    return X1, X2, X3, X4

def fourIndividualBools_into_fourBitList(X1:bool, X2:bool, X3:bool, X4:bool) -> list:
    """Takes a 4 variables and puts them into a list"""
    fourBitList = [X1, X2, X3, X4]
    return fourBitList

def eightBitList_into_individual_bools(Xbools: list) -> bool:
    """Takes a list 8 long and sepperates it into 8 seperate variables"""
    X1 = Xbools[0]
    X2 = Xbools[1]
    X3 = Xbools[2]
    X4 = Xbools[3]
    X5 = Xbools[4]
    X6 = Xbools[5]
    X7 = Xbools[6]
    X8 = Xbools[7]
    return X1, X2, X3, X4, X5, X6, X7, X8

def eightIndividualBools_into_eightBitList(X1:bool, X2:bool, X3:bool, X4:bool, X5:bool, X6:bool, X7:bool, X8:bool) -> list:
    """Takes a 8 variables and puts them into a list"""
    fourBitList = [X1, X2, X3, X4, X5, X6, X7, X8]
    return fourBitList

def format_truth_table(Xbools: list, Ybools: list) -> str:
    """Returns a String truth table taking in the binary 2DX List (input) and 2DY list (output)

        Input Table input example:\n
        XboolsEXAMPLE = [[0,0,1,1], [0,1,0,1]]\n
        YboolsEXAMPLE = [[0,0,0,1]]\n

        Truth Table output example:\n
        *------* \n   
        |0||0|1| \n   
        |1||1|0| \n  
        *------* \n                        
        *------* \n   
        |0|0||0| \n   
        |0|1||0| \n   
        |1|0||0| \n   
        |1|1||1| \n   
        *------* \n   
        *----------*\n
        |0|0|0||0|0|\n
        |0|0|1||1|0|\n
        |0|1|0||0|1|\n
        |0|1|1||1|1|\n
        |1|0|0||0|0|\n
        |1|0|1||1|0|\n
        |1|1|0||0|0|\n
        |1|1|1||1|1|\n
        *----------*\n
    EX:
    Xbools1 = [[0,1]]
    Ybools1 = [[0,1], [1,0]]

    Xbools2 = [[0,0,1,1], [0,1,0,1]]
    Ybools2 = [[0,0,0,1]]

    Xbools3 = [[0,0,0,0,1,1,1,1],[0,0,1,1,0,0,1,1],[0,1,0,1,0,1,0,1]]
    Ybools3 = [[0,1,0,1,0,1,0,1],[0,0,1,1,0,0,0,1]]
    """

    TruthTable = ""

    #for each layer down table do:
    for lenght in range(0, len(Xbools[0])):
        #for each layer wide do:
        for widthx in range(0, len(Xbools)):
            
            TruthTable += str(Xbools[widthx][lenght])

            TruthTable += "|"
        
        for widthy in range(0, len(Ybools)):
            TruthTable += "|"

            TruthTable += str(Ybools[widthy][lenght])
                
        TruthTable += "\n"

    return TruthTable
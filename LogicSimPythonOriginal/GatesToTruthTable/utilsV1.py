"""
    Name: utilsV2.py
    Author: Aidan Newberry
    Created: 10/3/2023
    Updated: 10/8/2023
    Purpose: A utility module with commonly used functions
"""
import ast

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


def get_float(prompt: str) -> float:
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
    
def get_int(prompt: str) -> int:
    """Gets a int from user with a try catch statement
    Uses prompt provided in function call
    """
    #Ask the user for an input based on the what parameter
    num = input(prompt)

    try:
        return int(num)
    
    except ValueError:
        print(f'You entered; {num}, which is not a integer .')
        print(f"Let's try that again.\n")

        #Call function from the beginning
        #this is a recursive function call
        return get_int(prompt)

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

def TakesAList_turnsinto_individualBools(Xbools: list) -> bool:
    listlen = len(Xbools)

    if listlen == 2:
        X1 = Xbools[0]
        X2 = Xbools[1]
        return X1, X2
    elif listlen == 4:
        X1 = Xbools[0]
        X2 = Xbools[1]
        X3 = Xbools[2]
        X4 = Xbools[3]
        return X1, X2, X3, X4
    elif listlen == 8:
        X1 = Xbools[0]
        X2 = Xbools[1]
        X3 = Xbools[2]
        X4 = Xbools[3]
        X5 = Xbools[4]
        X6 = Xbools[5]
        X7 = Xbools[6]
        X8 = Xbools[7]
        return X1, X2, X3, X4, X5, X6, X7, X8

def twoBitList_into_individual_bools(Xbools: list) -> bool:
    """Takes a list 2 long a sepperates it into 4 seperate variables"""
    X1 = Xbools[0]
    X2 = Xbools[1]
    return X1, X2

def twoIndividualBools_into_twoBitList(X1: bool, X2: bool) -> list:
    """Takes 2 variables and puts them into a list"""
    twoBitList = [X1, X2]
    return twoBitList

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

def sixteenBitList_into_individualbools(Xbools:list) -> bool:
    """Takes a 16 variale list and seperates it into sixteen seperate variables"""
    X1 = Xbools[0]
    X2 = Xbools[1]
    X3 = Xbools[2]
    X4 = Xbools[3]
    X5 = Xbools[4]
    X6 = Xbools[5]
    X7 = Xbools[6]
    X8 = Xbools[7]
    X9 = Xbools[8]
    X10 = Xbools[9]
    X11 = Xbools[10]
    X12 = Xbools[11]
    X13 = Xbools[12]
    X14 = Xbools[13]
    X15 = Xbools[14]
    X16 = Xbools[15]
    return X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, X15, X16

def sixteenindividualbools_into_sixteenbitlist(X1:bool, X2:bool, X3:bool, X4:bool, X5:bool, X6:bool, X7:bool, X8:bool, X9:bool, X10:bool, X11:bool, X12:bool, X13:bool, X14:bool, X15:bool, X16:bool) -> list:
    output = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, X15, X16]
    return output

def thirtytwobitlist_into_thirtytwoindividualbools(Xbools:bool) -> list:
    """Takes a 32 variale list and seperates it into 32 seperate variables"""
    X1 = Xbools[0]
    X2 = Xbools[1]
    X3 = Xbools[2]
    X4 = Xbools[3]
    X5 = Xbools[4]
    X6 = Xbools[5]
    X7 = Xbools[6]
    X8 = Xbools[7]
    X9 = Xbools[8]
    X10 = Xbools[9]
    X11 = Xbools[10]
    X12 = Xbools[11]
    X13 = Xbools[12]
    X14 = Xbools[13]
    X15 = Xbools[14]
    X16 = Xbools[15]
    X17 = Xbools[16]
    X18 = Xbools[17]
    X19 = Xbools[18]
    X20 = Xbools[19]
    X21 = Xbools[20]
    X22 = Xbools[21]
    X23 = Xbools[22]
    X24 = Xbools[23]
    X25 = Xbools[24]
    X26 = Xbools[25]
    X27 = Xbools[26]
    X28 = Xbools[27]
    X29 = Xbools[28]
    X30 = Xbools[29]
    X31 = Xbools[30]
    X32 = Xbools[31]
    return X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, X15, X16, X17, X18, X19, X20, X21, X22, X23, X24, X25, X26, X27, X28, X29, X30, X31, X32
    
def thirtyTwoindividualbools_into_thirtytwobitlist(X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, X15, X16, X17, X18, X19, X20, X21, X22, X23, X24, X25, X26, X27, X28, X29, X30, X31, X32) -> list:
    output = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, X15, X16, X17, X18, X19, X20, X21, X22, X23, X24, X25, X26, X27, X28, X29, X30, X31, X32]
    return output

def sixtyfourbitlist_into_sixtyfourindividualbools(Xbools:list):
    X1 = Xbools[0]
    X2 = Xbools[1]
    X3 = Xbools[2]
    X4 = Xbools[3]
    X5 = Xbools[4]
    X6 = Xbools[5]
    X7 = Xbools[6]
    X8 = Xbools[7]
    X9 = Xbools[8]
    X10 = Xbools[9]
    X11 = Xbools[10]
    X12 = Xbools[11]
    X13 = Xbools[12]
    X14 = Xbools[13]
    X15 = Xbools[14]
    X16 = Xbools[15]
    X17 = Xbools[16]
    X18 = Xbools[17]
    X19 = Xbools[18]
    X20 = Xbools[19]
    X21 = Xbools[20]
    X22 = Xbools[21]
    X23 = Xbools[22]
    X24 = Xbools[23]
    X25 = Xbools[24]
    X26 = Xbools[25]
    X27 = Xbools[26]
    X28 = Xbools[27]
    X29 = Xbools[28]
    X30 = Xbools[29]
    X31 = Xbools[30]
    X32 = Xbools[31]
    X33 = Xbools[32]
    X34 = Xbools[33]
    X35 = Xbools[34]
    X36 = Xbools[35]
    X37 = Xbools[36]
    X38 = Xbools[37]
    X39 = Xbools[38]
    X40 = Xbools[39]
    X41 = Xbools[40]
    X42 = Xbools[41]
    X43 = Xbools[42]
    X44 = Xbools[43]
    X45 = Xbools[44]
    X46 = Xbools[45]
    X47 = Xbools[46]
    X48 = Xbools[47]
    X49 = Xbools[48]
    X50 = Xbools[49]
    X51 = Xbools[50]
    X52 = Xbools[51]
    X53 = Xbools[52]
    X54 = Xbools[53]
    X55 = Xbools[54]
    X56 = Xbools[55]
    X57 = Xbools[56]
    X58 = Xbools[57]
    X59 = Xbools[58]
    X60 = Xbools[59]
    X61 = Xbools[60]
    X62 = Xbools[61]
    X63 = Xbools[62]
    X64 = Xbools[63]
    return X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, X15, X16, X17, X18, X19, X20, X21, X22, X23, X24, X25, X26, X27, X28, X29, X30, X31, X32, X33, X34, X35, X36, X37, X38, X39, X40, X41, X42, X43, X44, X45, X46, X47, X48, X49, X50, X51, X52, X53, X54, X55, X56, X57, X58, X59, X60, X61, X62, X63, X64

def sixtyfourindividualbools_into_sixtyfourbitlist(X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, X15, X16, X17, X18, X19, X20, X21, X22, X23, X24, X25, X26, X27, X28, X29, X30, X31, X32, X33, X34, X35, X36, X37, X38, X39, X40, X41, X42, X43, X44, X45, X46, X47, X48, X49, X50, X51, X52, X53, X54, X55, X56, X57, X58, X59, X60, X61, X62, X63, X64):
    output = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11, X12, X13, X14, X15, X16, X17, X18, X19, X20, X21, X22, X23, X24, X25, X26, X27, X28, X29, X30, X31, X32, X33, X34, X35, X36, X37, X38, X39, X40, X41, X42, X43, X44, X45, X46, X47, X48, X49, X50, X51, X52, X53, X54, X55, X56, X57, X58, X59, X60, X61, X62, X63, X64]
    return output

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

    #print("")
    #print(f"{Xbools}")
    #print(f"{Ybools}")
    #print("")

    #Xbools = [[0,0],[1,0],[0,1],[1,1]]
    #Ybools = [[0],[0],[1],[1]]

    #for each layer down table do:
    for lenght in range(0, len(Xbools)):
        #for each layer wide do:
        for widthx in range(0, len(Xbools[lenght])):
            
            TruthTable += str(Xbools[lenght][widthx])

            TruthTable += "|"
        
        for widthy in range(0, len(Ybools[lenght])):
            TruthTable += "|"

            TruthTable += str(Ybools[lenght][widthy])
                
        TruthTable += "\n"

    return TruthTable

def individualInput_into_TruthTableFormat(input: list) -> list:
    #[[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0]]]
    listlength = len(input)
    
    

    results = []

    #print(f"{listlength}, {lengthofinput}, {ammountofinputs}")
    
    for EachItemInInputList in range(0, listlength):

        tempList = []

        for EachInputInInputList in range(0, len(input[EachItemInInputList])):

            #print(input[EachItemInInputList][EachInputInInputList])

            for EachBoolInInputsList in range(0, len(input[EachItemInInputList][EachInputInInputList])):

                tempList.append(input[EachItemInInputList][EachInputInInputList][EachBoolInInputsList])
            
            
        results.append(tempList)

        #print(f"{results}")

    return results

def convert_string_to_list(string_list):
    """
    Funtion that takes a list in as a string and outputs a list variable
    # Input as a string
    string_list = input("Enter a string list in Python list format: ")

    # Convert the string to a real list
    result_list = convert_string_to_list(string_list)

    if result_list is not None:
    print("Converted list:", result_list)
    """
    try:
        # Use ast.literal_eval to safely evaluate the string as a Python literal
        real_list = ast.literal_eval(string_list)
        
        if type(real_list) == list:
            return real_list
        else:
            #print("Input is not a valid list.")
            return None
    except (SyntaxError, ValueError):
        #print("Input is not a valid list.")
        return None

def variableUnifier(variables:list):
        """a function to unify different types of 2d lists
        [[0], [0], [0]] -> [0, 0, 0]
        [[0, 0, 0, 0]] -> [0, 0, 0, 0]
        [[0, 0], [0, 0], [0]] -> [0, 0, 0, 0, 0]
        [[0, 0], 0] -> [0, 0, 0]"""
        output = []

        for var in variables:
            if type(var) == list:
                for varinvar in var:
                    output.append(varinvar)
            else:
                output.append(var)
        
        #print(f"{variables} len(variables) = {len(variables)} output = {output}")
        
        return output



class fileArchitect():
    """This class holds a bunch of functions for manipulaing files"""

    #Define Self variables
    def __init__(self):
        self.localfilename = ""
    
    def Create_File(self, locationfromuser: str, filenamefromuser: str, Truthtable: list) -> str:
        """Creates a file using the arguments, and makes a global name for the file so other blocks can access it"""
        try:
            if filenamefromuser == "" and locationfromuser == "":
                #create a file object
                Author = open(f"./{len(Truthtable)}_Combinations.txt", "x")
                self.localfilename = f"./{len(Truthtable)}_Combinations.txt"
                #print(f"Created file {len(answerstxt)}_equled_{mewanttxt}.txt in Downloads")
                return f"./{len(Truthtable)}_Combinations.txt in whatever location you ran this."
            elif filenamefromuser != "" and locationfromuser == "":
                #create a file object
                Author = open(f"./{filenamefromuser}.txt", "x")
                self.localfilename = f"./{filenamefromuser}.txt"
                #print(f"Created file {len(answerstxt)}_equled_{mewanttxt}.txt in Downloads")
                return f"./{filenamefromuser}.txt in whatever location you ran this."
            else:
                Author = open(f"{locationfromuser}{filenamefromuser}.txt", "x")
                self.localfilename = f"{locationfromuser}{filenamefromuser}.txt"
                #print(f"Created file{filenamefromuser}.txt in {locationfromuser}")
                return f"Created file{filenamefromuser}.txt in {locationfromuser}"
        except:
            print("Failed to create file because one with the same name allready exists")
            return "Critical Failure"
        #Close Author object
        Author.close()

    #function containging code about how to write a file   
    def Write_File(self, answerstxt: list) -> str:
        """Using a list parametere this function will write it to the file defined in the create file function"""
        try:
            Author = open(self.localfilename, "w")
            Author.write(str(answerstxt)) 
            Author.close()
            return "Success!"
        except:
            print("Something Went wrong when writing the file")
            return "Critical Failure"

    #function containging code about how to read a file
    def Read_File(self) -> str:
        """Returns a string containing all the information on the file"""
        try:
            Author = open(self.localfilename, "r")
            _contents = Author
            Author.close()
            return _contents
        except:
            print("Something Went wrong when reading the file")
            return "Critical Failure"    

    
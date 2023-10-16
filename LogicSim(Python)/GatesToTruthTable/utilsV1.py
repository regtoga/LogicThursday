"""
    Name: utilsV1.py
    Author: Aidan Newberry
    Created: 10/3/2023
    Updated: 10/8/2023
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

"""the goal of this file is to take a input function: F = A'B + AB' and output the result as a truth table, and as a function: F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7)"""

class TruthTableToGates():
    def __init__(self,function:str="") -> None:
        """class can be initialized with a function to solve value."""
        #main var to witch everything will be derived.
        self.functionToSolve = function
        self.justfunction = ""

        #answer vars
        self.TruthTable = ""
        self.AnswerFunction = ""

        #working vars
        self.numvariables = 0
        ValidInputChars = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')

        #start with init function code to make everything work:
        
        #This bit removes the start of the function off if there is one.
        startapending = 1
        
        leninput = len(self.functionToSolve)
        for index in range(0, leninput):
            #this is the variable for the current char
            currentchar = self.functionToSolve[index]

            if currentchar.lower() == "f":
                startapending = 0

            #if all conditions pass start 
            if (startapending == 1) and (currentchar != " "):
                self.justfunction += currentchar

            #this is after the rest of the if's because i didnt want to append the ='s sign
            if currentchar == "=":
                startapending = 1

        print(self.justfunction)





    def __del__(self) -> None:
        pass

    def set_functionToSolve(self, function:str) -> int:
        """Sets the function to solve value to whatever you input"""
        self.functionToSolve = function

    def get_functionToSolve(self) -> str:
        """Returns the function to solve value"""
        return self.functionToSolve

    #start programing here
    
    def get_TruthTable(self) -> str:
        """This function should solve for the truth table of the input function"""
        pass

    def get_AnswerFunction(self,MinorMax="m") -> str:
        """This function should return a function such as: F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7)"""
        pass


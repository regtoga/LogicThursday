"""the goal of this file is to take a input function: F = A'B + AB' and output the result as a truth table, and as a function: F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7)"""

import sqlite3

class TruthTableToGates():
    def __init__(self,function:str="") -> None:
        """class can be initialized with a function to solve value."""
        #main var to witch everything will be derived.
        self.functionToSolve = function
        self.justfunction = ""
        #either min or max terms
        self.minterms = []
        self.maxterms = []

        #answer vars
        self.TruthTable = ""
        self.AnswerFunction = ""

        #working vars
        self.largestvarnum = 0
        self.justfunctioninenglish = ""
        self.ValidInputChars = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')

        #start with init function code to make everything work:
        
        #This bit removes the start of the function off if there is one.
        startapending = 1
        isFfound = False
        
        leninput = len(self.functionToSolve)
        for index in range(0, leninput):
            #this is the variable for the current char
            currentchar = self.functionToSolve[index]

            if currentchar.lower() == "f" and isFfound == False:
                startapending = 0
                isFfound = True

            #if all conditions pass start 
            if (startapending == 1) and (currentchar != " "):
                self.justfunction += currentchar

            #this is after the rest of the if's because i didnt want to append the ='s sign
            if currentchar == "=":
                startapending = 1

        self.justfunction.replace(" ", "")

        #This commented print function would output just the logic portion of the input
        #print(self.justfunction)
                
        #Take the justfunction of the input and find the largest var it uses, such as A'BCE = E -> the num of inputs is 5
        #the second part of the for loop makes the function in the correct notation in english
        lenjustfunction = len(self.justfunction)
        self.justfunctioninenglish += "("
        for index in range(0, lenjustfunction):
            if self.justfunction[index] in self.ValidInputChars:
                currentvarnum = self.ValidInputChars.index(self.justfunction[index])
                if self.largestvarnum < currentvarnum:
                    self.largestvarnum = currentvarnum

                #start the english translation
                if (lenjustfunction > index +1) and (self.justfunction[index+1] == "'"):
                    self.justfunctioninenglish += f"(NOT({self.ValidInputChars[self.largestvarnum]}))"
                else:
                    self.justfunctioninenglish += f"({self.ValidInputChars[self.largestvarnum]})"

                #essentially add 'OR' to any string that should have it
                if ((lenjustfunction > index +1) and (self.justfunction[index+1] in self.ValidInputChars)) or ((lenjustfunction > index+2) and ((self.justfunction[index+1] == "'") and (self.justfunction[index+2] in self.ValidInputChars))):
                    self.justfunctioninenglish += f" OR "

            elif self.justfunction[index] == "+":
                self.justfunctioninenglish += f") AND ("

        self.justfunctioninenglish += ")"

        #this is a waste of code and time but its here just incase somebody cares :)
        #print(self.justfunctioninenglish)

        #would show the largest num calculated to be inside the input function
        #print(f"Largest var num = {self.largestvarnum}, {self.ValidInputChars[self.largestvarnum]}")


        #create a list of bools that will be counted to provide the TruthTable
        inputslist = [False]
        termnum = -1
        
        runOne = True
        while all(value for value in inputslist) == False:
            termnum +=1

            if runOne == True:
                #remove initial value to make function work properly
                inputslist.clear()

                for index in range(0, self.largestvarnum+1):
                    inputslist.append(False)
                    runOne = False
                #print the initial inputs list
                #print(inputslist)
            else:
                #make a recursive function to do counting
                inputslist = binaryCountingWithList(inputslist)
            
            #Do calculation!
            
            functionoutput = calculateFunctionOutput(self.justfunction, inputslist)
            #formats a way for the programmer to understand both the function inputs and outputs
            #print(f"{inputslist} = {functionoutput}")

            if functionoutput == False:
                self.maxterms.append(termnum)
            else:
                self.minterms.append(termnum)

        #temp to show output of function
        #print(f"minterms: {self.minterms},\nMaxterms: {self.maxterms}")
    
            
    def __del__(self) -> None:
        pass

    def set_functionToSolve(self, function:str) -> int:
        """Sets the function to solve value to whatever you input"""
        self.functionToSolve = function

    def get_functionToSolve(self) -> str:
        """Returns the function to solve value"""
        return self.functionToSolve
    
    def get_inputInEnglish(self) -> str:
        """returns the input function in an english format"""
        return self.justfunctioninenglish

    #start programing here
    
    def get_TruthTable(self) -> str:
        """This function should solve for the truth table of the input function"""
        #Create an SQL table baised on the dimentions of the inputs and the calculated minterms
        pass

    def get_AnswerFunction(self,MinorMax="m") -> str:
        """This function should return a function such as: F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7)"""
        #Create a original Functions baised on the calculated minterms
        output = "F("

        for index in range(0, self.largestvarnum):
            if index != self.largestvarnum-1:
                output += f"{self.ValidInputChars[index]},"
            else:
                output += f"{self.ValidInputChars[index]}"
        
        output += f") = Z'{MinorMax}"

        if MinorMax == "m":
            output += f"{tuple(self.minterms)}"
        else:
            output += f"{tuple(self.maxterms)}"

        return output


#Nessesary Binary functions = AND, OR, NOT
def NOT(input:bool) -> bool:
    """Literally will just invert a bool"""
    return not(input)

def AND(input1:bool, input2:bool):
    """provides AND gate functionallity"""
    return input1 and input2

def OR(input1:bool, input2:bool):
    """provides OR gate functionality"""
    #litearlly an or function
    return input1 or input2
 
def binaryCountingWithList(list:list) -> list:
    "function that will do binary counting on a list of boolean values"
    listlen = len(list)
    index = listlen-1

    #all that this does is if the end of the list is already true when NOT'ing it it will make the next digit the new end and repeat the process
    while index >= 0:
        currentlistvalue = list[index]
        if currentlistvalue != True:
            list[index] = not(list[index])
            break
        list[index] = not(list[index])

        index -=1

    return list

def calculateFunctionOutput(function:str, inputs:list) -> bool:
    """This function takes a function input such as A'BCD+AB'C' and an input and outputs the result """
    ValidInputChars = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
    answer = 0
    oldanswers = []
    
    #do all the AND'ing
    firstNumInSequence = True
    for index in range(0, len(function)):
        #check if the current index is a ' or + if it is and the last input was a ' append the current answer to the queue
        if (function[index] == "'") or (function[index] == "+"):
            if (function[index] == "+"):
                firstNumInSequence = True
                if function[index-1] == "'":
                    oldanswers.append(answer)
                    answer = 0
                      
        else:
            num = inputs[ValidInputChars.index(function[index])]

            #NOT opperation leading into an AND opperation on function[indexl]
            if (index+1 < len(function)) and (function[index+1] == "'"):
                if firstNumInSequence == True:
                    answer = NOT(num)
                    firstNumInSequence = False
                else:
                    answer = AND(NOT(num), answer)

            #AND opperaton when at the end of a group of numbers
            elif (index+1 < len(function)) and (function[index+1] == "+"):
                if firstNumInSequence == True:
                    oldanswers.append(num)
                    firstNumInSequence = False
                else:
                    oldanswers.append(AND(num, answer))
                answer = 0

            #AND Opperation on the numbers 
            else:
                if firstNumInSequence == True:
                    answer = num
                    firstNumInSequence = False
                else:
                    answer = AND(num, answer)
    
    #add the last answer the the old answers list
    oldanswers.append(answer)
    answer = 0

    #take the list of answers and OR them together
    for index in oldanswers:
        if index == True:
            return True

    return False
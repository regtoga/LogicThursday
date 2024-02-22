#This File should ONLY be the CLI the rest goes inside of the TruthTableToGates object

import TruthTableToGatesThinker as Thinker

"""
    1. Ask if user has a preformatted TruthTable if so let them enter it in one line, else continue though steps 2-4
        -preformatted TruthTable: F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7) or F(A,B,C) = Z'M(2,3,4,5)+Z'd(6,7).

    2. Get Ammount of input variables from user -(optional, can compute based of of 3,4 but computer guess may be smaller than user desires).
    3. Get MinTerms from user in [0,1,2,4,6] format, Also Ask If we are computing for Maxterms instead.
    4. Get Dont Cares from userin [8,9,10] format -(optional, arnt required).

    5. Return User Result in "f = CD + A'B'C' + ABD + ABC" format, allow them to save it to a text file or something similar.

    6.Do it again!
"""

def helpme():
    """This function if working properly will return a working input notation"""

    #Help for step 1:
    print("""
        Ok so you asked for help... I am not a very good teacher but i will try my best:
        
        The base Function: F(w)=Z'x(y)+Z'd(z)
        A propperly submitted function: F(A,B,C)=Z'm(2,3,4,5)+Z'd(6,7)

        Lets disect what information you need to submit for successful opperation of the program.
        1. F(w), The first part of the function needs 'w' replaced with the input variables. These- 
        can be any english letter or character singular. Ex: F(A,B,C) or F(1,2,3). Note this step-
        is actually optional and you can leave it blank.
        """)
    
    #iscorrect is a variable used to ask the user if his echoed input looks correct
    iscorrect = "n"

    userinputvars = input("Now its your turn enter your input variables: ")
    if userinputvars != "":
        iscorrect = input(f"Your input: F({userinputvars}), Does it look correct? (y/n): ")
    else:
        iscorrect = "y"

    while (iscorrect).lower() != "y":
        userinputvars = input("ok try again, Enter your input variables: ")
        iscorrect = input(f"Your input: F({userinputvars}), Does it look correct? (y/n): ")

    #used to store the final output
    finaluserinput = ""

    if userinputvars != "":
        finaluserinput += f"F({userinputvars}) = "

    print("\nThanks, Continuing to step 2...\n")

    #-------------------------------------------------------------------

    #help for step 2:
    print("""
        2. The first required step in this function is telling me what your are solving this-
        Truthtable for. If for a given input you are searching for the binary "True" ouputs then-
        you are solving for minterms. If you are searching for Maxterms then the opposite is true.
        
        here is an example:
        INPUTS   OUTPUTS
        000 | 1 <-minterm (m0)
        001 | 0                <-MAXterm (M1)
        010 | 1 <-minterm (m2)
        011 | 0                <-MAXterm (M3)
        100 | 1 <-minterm (m4)
        101 | 1 <-minterm (m5)
        110 | 0                <-MAXterm (M6)
        111 | 0                <-MAXterm (M7)
        """)
    
    #iscorrect is a variable used to ask the user if his echoed input looks correct
    iscorrect = "n"

    userinputTerms = input("Now are you solving for Maxterms (M) or minterms (m)? : ")
    
    #correct user input if incorrect:
    if (userinputTerms.lower() == "maxterms") or (userinputTerms.lower() == "maxterm"):
        userinputTerms = "M"
    elif (userinputTerms.lower() == "minterms") or (userinputTerms.lower() == "minterm"):
        userinputTerms = "m"

    iscorrect = input(f"Your input: Z'{userinputTerms}(), Does it look correct? (y/n): ")

    #repeat untill correct everthing in step 2:
    while (iscorrect).lower() != "y":
        userinputTerms = input("Ok so again are you solving for Maxterms (M) or minterms (m)? : ")
    
        #correct user input if incorrect:
        if (userinputTerms.lower() == "maxterms") or (userinputTerms.lower() == "maxterm"):
            userinputTerms = "M"
        elif (userinputTerms.lower() == "minterms") or (userinputTerms.lower() == "minterm"):
            userinputTerms = "m"

        iscorrect = input(f"Your input: Z'{userinputTerms}(), Does it look correct? (y/n): ")

    finaluserinput += f"Z'{userinputTerms}"
        
    print("\nThanks, Continuing to step 3...\n")

    #-------------------------------------------------------------------

    whatterm = ""

    if userinputTerms == "M":
        whatterm = "Maxterm"
    else:
        whatterm = "minterm"

    #help for step 3:
    print(f"""
        2. The second and last required step for this program is telling me what your {whatterm}s are.
        
        as you can see in this example: you need to give me the numbers of the {whatterm}s.
        The minterms will look like this 1,2,3 or 3,7,100 or 9.
        Example TruthTable:
        INPUTS   OUTPUTS
        000 | 1 <-minterm (m0)
        001 | 0                <-MAXterm (M1)
        010 | 1 <-minterm (m2)
        011 | 0                <-MAXterm (M3)
        100 | 1 <-minterm (m4)
        101 | 1 <-minterm (m5)
        110 | 0                <-MAXterm (M6)
        111 | 0                <-MAXterm (M7)
        """)

    #iscorrect is a variable used to ask the user if his echoed input looks correct
    iscorrect = "n"

    minormaxtermsvars = input(f"Now its your turn enter your {whatterm} numbers: ")
    iscorrect = input(f"Your input: {finaluserinput}({minormaxtermsvars}), Does it look correct? (y/n): ")


    while (iscorrect).lower() != "y":
        minormaxtermsvars = input(f"Ok try again, Enter your {whatterm} numbers: ")
        iscorrect = input(f"Your input: {finaluserinput}({minormaxtermsvars}), Does it look correct? (y/n): ")

    #add to result to the end.
    finaluserinput += f"({minormaxtermsvars})"

    print("\nThanks, Continuing to step 4...\n")

    #-------------------------------------------------------------------

    #help for step 4:
    print(f"""
        2. This is the last step, and it is completely optional. You need to tell me what your dont's are.
        don't cares are conditions that you expect will never get triggered in actual use, that is why its called "dont care"
        
        as you can see in this example: you need to give me the numbers of the dont cares, here they are 5,7 .
        The dontcares will look like this 1,2,3 or 3,7,100 or 9.
        Example TruthTable:
        INPUTS   OUTPUTS
        000 | 1 <-minterm (m0)
        001 | 0                <-MAXterm (M1)
        010 | 1 <-minterm (m2)
        011 | 0                <-MAXterm (M3)
        100 | 1 <-minterm (m4)
        101 | x <-dontcare (d5)
        110 | 0                <-MAXterm (M6)
        111 | x                <-dontcare (d7)
        """)

    #iscorrect is a variable used to ask the user if his echoed input looks correct
    iscorrect = "n"

    dontcares = input(f"Now its your turn enter your dontcares: ")
    #check if input correct
    if dontcares == "":
        iscorrect = "y"
    else:
        iscorrect = input(f"Your input: Z'd({dontcares}), Does it look correct? (y/n): ")

    while (iscorrect).lower() != "y":
        minormaxtermsvars = input(f"Ok try again, Enter your dontcares: ")
        iscorrect = input(f"Your input: Z'd({dontcares}), Does it look correct? (y/n): ")

    #add to result to the end.
    if dontcares != "":
        finaluserinput += f"Z'd({dontcares})"

    print("\nThanks!\n")

    #-------------------------------------------------------------------
    
    return finaluserinput

#program starts here

userinput = ""

while True:
    print("At anytime if you need help type 'help'!")
    userinput = input("Enter a truthtable equasion in F()=Z'm()+Z'd() format: ")

    if (userinput).lower() == "exit":
        break
    elif (userinput).lower() == "help":
        #Help The user to the best of my ability
        userinput = helpme()
        print("You Completed the help screen!\n")
    
    print("Answer: ")
    
    #make TtoG object
    TtoG = Thinker.TruthTableToGates(userinput)
    print(f"TruthTable      : {TtoG.get_TruthTable()}")
    print(f"Number of Inputs: {TtoG.get_NumInputVars()}")
    print(f"Min or Max      : {TtoG.get_MinorMax()}")
    print(f"minterms        : {TtoG.get_Minterms()}")
    print(f"Maxterms        : {TtoG.get_Maxterms()}")
    print(f"Dont Cares      : {TtoG.get_DontCares()}")
    print(f"{TtoG.get_Answer()}")
    print(f"Reformatted TruthTable String: {TtoG.TruthTableDataIntoTruthTable()}")
    print("")

print("thanks for using my program, it means a lot to me!")




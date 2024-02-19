#This File is COMPLETELY dedicated to Taking a truthtruth table and minimazing it.

"""
    The prime objective of this program is to take a preformed Truthtable and minmize it.
    -preformatted TruthTable: F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7) or F(A,B,C) = Z'M(2,3,4,5)+Z'd(6,7)

    This is done in four steps :          (might be more depending on how many variables there are but i have only solved one so IDK)
    Step 1:
        Group All the minterms (and possibly Maxterms) by ammount of change in their Binary Representation

    Step 2:
        Find Match Pairs by comparing EVERY minterm in a group with every other minterm in group +1 of that minterm.
        The Comparison must happen between the Binary Representation of one minterm and the next, though we only move them on to the next step-
        if they are different by one variable. We represent the different variable by an Underscore in place of the 0/1.
    
    Step 3:
        repeat step 2 untill there are no more matched pairs to be found, (might be 2 groups forever but IDK).

    Step 4:
        After all matched pairs/Prime implicants are found we need to make a new table called the Prime Implicant Table:
        This table has one purpose, make it obious which minterms used in a prime implicant show up only once. If If there is a pair of two-
        that only show up once we write down the Prime Implicants in the ouput function and go find if there are any more. If there arnt we have our answer.
"""

class TruthTableToGates():
    """Creates a TruthTableToGates object, this object has the ability to be created with a TruthTable allready made for it,
    or it has the ability to have the information straight up given to it.
    """
    def __init__(self, TruthTable:str="") -> None:
        self.NumInputVars = 0
        self.MinorMax = "UNDF"
        self.Minterms = []
        self.Maxterms = []
        self.DontCares = []

        """
        The init takes A TruthTable str and will convert it into all the nessesary information.
        
        Format input: F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7) or F(A,B,C) = Z'M(2,3,4,5)+Z'd(6,7)
        """
        self.TruthTable = TruthTable

        #if truthtable isn't empty:
        if TruthTable != "":
            #---------------------------------------------------------------------------
            #calculate var ammount baised off of input ammount

            #ValidInputChars = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
            BeginCounting = 0

            #iterate though the truthTable and find the ammout of Input Vars
            for character in self.TruthTable:

                if character == '(':
                    BeginCounting = 1
                elif character == ')':
                    BeginCounting = 0
                    break

                if BeginCounting == 1 and (character != ',' and character != '('):
                    self.NumInputVars += 1
            #---------------------------------------------------------------------------
            #Determine if we are solving for minterms or Maxterms
            
            #itterate though every value of TruthTable and find the portion where the minterm or maxterm is stored.
            for character in self.TruthTable:
                if character == "'":
                    BeginCounting = 1
                elif character == '(' and BeginCounting == 1:
                    BeginCounting = 0
                    break

                if BeginCounting == 1:
                    if character == 'm':
                        self.MinorMax = "minterms"
                
                    if  character == 'M':
                        self.MinorMax = "Maxterms"
                
            
            #---------------------------------------------------------------------------
            #make a list of the minterms (or Maxterms that is what we are solveing for)
            #format input again for reference: F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7) or F(A,B,C) = Z'M(2,3,4,5)+Z'd(6,7)
            characterbefore = ''
            for character in self.TruthTable:
                if character.lower() == 'm' and characterbefore == "'":
                    BeginCounting = 1
                elif character == ')' and BeginCounting == 1:
                    BeginCounting = 0
                    break

                shouldhavebeenconbined = 0

                if BeginCounting == 1:
                    if  (character != ',' and character != '(') and character.lower() != 'm':
                        
                        #nested if's to tell if the char before should have been combined with the char after to make a single number
                        if  (characterbefore != ',' and characterbefore != '(') and characterbefore.lower() != 'm':
                            #if the number is more than 9 this will happen
                            if self.MinorMax == 'minterms':
                                #Remove incorrect value from end of list
                                self.Minterms.pop()

                                #append correct terms to end of list
                                self.Minterms.append(int(characterbefore+character))

                            elif self.MinorMax == 'Maxterms':
                                #Remove incorrect value from end of list
                                self.Maxterms.pop()

                                #append correct terms to end of list
                                self.Maxterms.append(int(characterbefore+character))
                            #set the character before the the sum of two characters 2 + 3 = 23
                            characterbefore = characterbefore + character
                            shouldhavebeenconbined = 1
                                
                        
                        #aslong as the number is 0-9 this will happen
                        if shouldhavebeenconbined == 0:
                            if self.MinorMax == 'minterms':
                                self.Minterms.append(int(character))
                            elif self.MinorMax == 'Maxterms':
                                self.Maxterms.append(int(character))

                #this is here to make shure that there is a "'m" in the sentence because i was getting errors
                if shouldhavebeenconbined == 0:
                    characterbefore = character


            #---------------------------------------------------------------------------
            #make a list of the dont cares, works same way as making a list for the min/Max terms.
            zeroDontCares = 0
            characterbefore = ''              

            for character in self.TruthTable:
                #var for telling if the char that i just checked should have had the next char added to it aswell.
                shouldhavebeenconbined = 0

                if character.lower() == 'd' and characterbefore == "'":
                    BeginCounting = 1
                elif character == ')' and BeginCounting == 1:
                    BeginCounting = 0
                    break

                if BeginCounting == 1:
                    if  (character != ',' and character != '(') and character.lower() != 'd':
                        #if the last character was a number and the new char was a number add them together to get one num
                        if  (characterbefore != ',' and characterbefore != '(') and characterbefore.lower() != 'd':
                            #take the problem off the end of the list
                            self.DontCares.pop()

                            shouldhavebeenconbined = 1
                            self.DontCares.append(int(characterbefore + character))
                            characterbefore = characterbefore + character

                        if shouldhavebeenconbined == 0:
                            self.DontCares.append(int(character))

                #this is here to make shure that there is a "'d" in the sentence because i was getting errors
                
                if shouldhavebeenconbined == 0:
                    characterbefore = character

            #indicate that there might not be any dont cares
            if len(self.DontCares) == 0:
                zeroDontCares = 1

            #---------------------------------------------------------------------------
            #if the Ammount of Variables is incorrect or not given for the given minterms, or dont cares recalculate the ammount of given vars
            largestnumberfound = 0

            #find the largest minterm in the given set of numbers.
            if zeroDontCares == 0:
                if self.MinorMax == 'minterms':
                    largestnumberfound = max([max(self.Minterms),max(self.DontCares)])
                elif self.MinorMax == 'Maxterms':
                    largestnumberfound = max([max(self.Maxterms),max(self.DontCares)])
            else:
                #if there are zero Dont Cares dont worry about them in the final calculation
                if self.MinorMax == 'minterms':
                    largestnumberfound = max(self.Minterms)
                elif self.MinorMax == 'Maxterms':
                    largestnumberfound = max(self.Maxterms)

            i = 0
            b = 0
            while b < largestnumberfound:
                i += 1
                b = 2**i
            #print(f"The largest number that fit under {largestnumberfound} was {i} because 2**{i} = {2**i}")

            if self.NumInputVars < i:
                self.NumInputVars = i  

            #---------------------------------------------------------------------------
            #from the minterms (or Maxterms) make a list of the Maxterms (or minterms) taking in account for the don't cares   
            counter = 0
            if self.MinorMax == 'minterms':
                while counter < 2**self.NumInputVars:
                    if (counter not in self.Minterms) and (counter not in self.DontCares):
                        #if a minterm is not in either in minterm or dont care then it must be a Maxterm.
                        self.Maxterms.append(counter)
                    counter += 1

            elif self.MinorMax == 'Maxterms':
                while counter < 2**self.NumInputVars:
                    if (counter not in self.Maxterms) and (counter not in self.DontCares):
                        #if a Maxterm is not in either in Maxterm or dont care then it must be a minterm.
                        self.Minterms.append(counter)
                    counter += 1
            
            #---------------------------------------------------------------------------


    #define Getters and setters for the main attrubutes of the TruthTable
    def get_TruthTable(self):
        """Returns the truthTable if one was given at the start."""
        return self.TruthTable    

    def get_NumInputVars(self) -> int:
        """Returns number of the function's input vars.
        This number is what makes this problem so difficult because as the number increases the combinations possible ='s the square root of the numvars. var^2"""
        return self.NumInputVars

    def get_MinorMax(self) -> str:
        """Returns A string that will read "min" or "Max", if the value hasn't been set yet "UNDF". 
        This will be used in the object to decide whether i should use the minterm algorithm or Maxterm algorithm. """
        return self.MinorMax

    def get_Minterms(self) -> list:
        """Returns a list of minterms of the object, These are simply the location in the truthtable where the answer is one!"""
        return self.Minterms
    
    def get_Maxterms(self) -> list:
        """Returns a list of Maxterms of the object, These are simply the location in the truthtable where the answer is zero!"""
        return self.Maxterms
    
    def get_DontCares(self) -> list:
        """Returns a list of locations in the truthtable where the output value of the function doesnt end up mattering.
        Essentially think about it as a way of saying i DONT CARE what this output is. "When i designed the truthtable i didnt think this output case was even possible to trigger." """
        return self.DontCares
    
    #Actual Algorithm goes here:

    def step1(self) -> bool:
        """
        Step 1:
            Group All the minterms (and possibly Maxterms) by ammount of change in their Binary Representation.
        """
        return 0
    
    def step2(self) -> bool:
        """
        Step 2:
            Find Match Pairs by comparing EVERY minterm in a group with every other minterm in group +1 of that minterm.
            The Comparison must happen between the Binary Representation of one minterm and the next, though we only move them on to the next step-
            if they are different by one variable. We represent the different variable by an Underscore in place of the 0/1.
        """
        return 0
    
    def step3(self) -> bool:
        """
        Step 3:
            repeat step 2 untill there are no more matched pairs to be found, (might be 2 groups forever but IDK).
        """
        return 0
    
    def step4(self) -> bool:
        """
        Step 4:
            After all matched pairs/Prime implicants are found we need to make a new table called the Prime Implicant Table:
            This table has one purpose, make it obious which minterms used in a prime implicant show up only once. If If there is a pair of two-
            that only show up once we write down the Prime Implicants in the ouput function and go find if there are any more. If there arnt we have our answer.
        """
        return 0
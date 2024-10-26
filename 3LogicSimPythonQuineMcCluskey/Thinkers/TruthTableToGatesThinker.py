#This File is COMPLETELY dedicated to Taking a truthtruth table and minimazing it.

import sqlite3

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
    def __init__(self, TruthTable:str="", KeepResults:str="") -> None:
        self.NumInputVars = 0
        self.MinorMax = "UNDF"
        self.Minterms = []
        self.Maxterms = []
        self.DontCares = []

        #define variable that is used to keep track of how many matched pairs tables
        self.numbermatchedpairstables = 0

        #vars for defining the num of min and max terms.
        self.numMax = 0
        self.nummin = 0

        self.ValidInputChars = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')

        self.answer = ""

        """
        The init takes A TruthTable str and will convert it into all the nessesary information.
        
        Format input: F(A,B,C) = Z'm(2,3,4,5)+Z'd(6,7) or F(A,B,C) = Z'M(2,3,4,5)+Z'd(6,7)
        """
        self.TruthTable = TruthTable

        #if truthtable isn't empty:
        if TruthTable != "":
            #---------------------------------------------------------------------------
            #calculate var ammount baised off of input ammount

            #ValidInputChars = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
            BeginCounting = 0

            #iterate though the truthTable and find the ammout of Input Vars
            firstchar = ''
            for character in self.TruthTable:
                if firstchar == '':
                    firstchar = character
                    if (firstchar).lower() != 'f':
                        break

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
                b = (2**i) - 1
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
            #Calculate num of min and Max terms:
                self.nummin = len(self.Minterms)
                self.numMax = len(self.Maxterms)   

            #---------------------------------------------------------------------------
            #Make a Database for the program to utilize later
            self.databasename = f"TempDatabaseforTruthTableThinker.db"

            #if KeepReuslts not nothing the table will not be cleared at the end.
            if KeepResults != "":
                self.databasename = KeepResults

            #make a connecction and a self.cursor | self.connection creates a file if one doesnt exist | self.cursor is how we interact with the db.
            self.connection = sqlite3.connect(self.databasename)
            self.cursor = self.connection.cursor()

            #I think that dropping a table will clear it, so that is what this does
            SQL = """
            DROP TABLE IF EXISTS stl_matchedpairs1;
            DROP TABLE IF EXISTS stl_matchedpairs2;
            DROP TABLE IF EXISTS stl_matchedpairs3;
            DROP TABLE IF EXISTS stl_matchedpairs4;
            DROP TABLE IF EXISTS stl_matchedpairs5;
            DROP TABLE IF EXISTS stl_matchedpairs6;
            DROP TABLE IF EXISTS stl_matchedpairs7;
            DROP TABLE IF EXISTS stl_primeimplicanttable;
            """

            #Run the SQL
            self.cursor.executescript(SQL)

            #----Create the table for when we group by number of 1's in the bin rep
            #The range of the number is the number of tables im generating for matched pairs
            i = 0
            while i in range(7):
                SQL = f"""
                CREATE TABLE IF NOT EXISTS stl_matchedpairs{i+1}(
                    PK_id INTEGER PRIMARY KEY,
                    groupp INTEGER,             
                    matched_pairs TEXT,
                    bin_rep TEXT,
                    checked BLOB  --literaly not binary
                )
                """
                i += 1
                self.cursor.execute(SQL)


            #makes the SQL code for all of the numbers in the Prime Implicant table
            termforinput = ""

            if self.MinorMax == 'minterms':
                for term in self.Minterms:
                    termforinput += f",m{term} TEXT"

            elif self.MinorMax == 'Maxterms':
                for term in self.Maxterms:
                    termforinput += f",M{term} TEXT"


            #This SQL will generate the table utilizing the ammount of min/max terms and other stuff.
            SQL = f"""CREATE TABLE IF NOT EXISTS stl_primeimplicanttable(pk_id INTEGER PRIMARY KEY,prime_implicants TEXT,matched_pairs_involved{termforinput})"""

            self.SQLforImplicantsTable = SQL

            self.cursor.execute(SQL)

    def __del__(self):
        #when the program is garbage collecting im going to have it deleate all the contents of the database aslong as the name is the default one

        #This code will tell me if the self.databasename exists yet, which it should but im getting an error so im going to make it work
        try:
            defaultname = "TempDatabaseforTruthTableThinker.db"
        
            if self.databasename == defaultname:
                #I think that dropping a table will clear it, so that is what this does
                SQL = """
                DROP TABLE IF EXISTS stl_matchedpairs1;
                DROP TABLE IF EXISTS stl_matchedpairs2;
                DROP TABLE IF EXISTS stl_matchedpairs3;
                DROP TABLE IF EXISTS stl_matchedpairs4;
                DROP TABLE IF EXISTS stl_matchedpairs5;
                DROP TABLE IF EXISTS stl_matchedpairs6;
                DROP TABLE IF EXISTS stl_matchedpairs7;
                DROP TABLE IF EXISTS stl_primeimplicanttable;
                """

                #Run the SQL
                self.cursor.executescript(SQL)

                #VACUUM should reallocate the disk space after deleating everything in the SQL before
                self.connection.execute("VACUUM")

            self.cursor.close()
            self.connection.close()
        except Exception as e:
            print(f"__del__ failed in the TruthTableToGatesThinker.py because, {e}")


        


    def TruthTableDataIntoTruthTable(self) -> str:
        """When this is ran it will return a new Truth Table value and set the inside 'self.TruthTable' var to it aswell aslong as its valid, 
        will only return a value if all data that it needs is allready defined!"""

        #Make a string array of the input chars
        currentinputs = ""
        for i in range(self.NumInputVars):
            if i == 0:
                currentinputs += f"{self.ValidInputChars[i]}"
            else:
                currentinputs += f",{self.ValidInputChars[i]}"

        #turn the list of min/max terms into a string list
        currentminormax = ""
        if self.MinorMax == "minterms":
            for i in range(0, len(self.Minterms)):
                if i == 0:
                    currentminormax += f"{self.Minterms[i]}"
                else:
                    currentminormax += f",{self.Minterms[i]}"

        elif self.MinorMax == "Maxterms":
            for i in range(0, len(self.Maxterms)):
                if i == 0:
                    currentminormax += f"{self.Maxterms[i]}"
                else:
                    currentminormax += f",{self.Maxterms[i]}"

        #find the list of dont cares
        currentdontcare = ""
        for i in range(0, len(self.DontCares)):
            if i == 0:
                currentdontcare += f"{self.DontCares[i]}"
            else:
                currentdontcare += f",{self.DontCares[i]}"

        dontcare = ""
        if currentdontcare != "":
            dontcare = f"+Z'd({currentdontcare})"

        self.TruthTable = f"F({currentinputs})=Z'{self.MinorMax[0]}({currentminormax})" + dontcare

        return self.TruthTable

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
    
    def get_Answer(self) -> str:
        """Returns the answer that the object has computed, 
        this will just return an error message with the original truthtable if the answer hasnt been found yet

        *As of writing this the TruthTable does not generate if one was not given as the program initialized."""
        if self.answer == "":
            self.answer = f"ERROR: The output has not yet been solved for: {self.TruthTable}"

        return self.answer
    
    def print_all_TABLES(self) -> str:
        """Prints all tables in Database"""

        answer = ""

        for counter in range(7):
            #Fetch all records from the first matched pairs table
            self.cursor.execute(f"Select * FROM stl_matchedpairs{counter+1}")
            publisher_data = self.cursor.fetchall()

            if publisher_data != []:
                answer = f"{answer}\nAll Contents of matched pairs{counter+1}:"
                for publisher in publisher_data:
                    answer = f"{answer}\n{publisher}"
                
                answer = f"{answer}\n"

        #Fetch all records from the first matched pairs table
        self.cursor.execute(f"Select * FROM stl_primeimplicanttable")
        publisher_data = self.cursor.fetchall()

        if publisher_data != []:
            answer = f"{answer}\nAll Contents of prime implicants table:"
            for publisher in publisher_data:
                answer = f"{answer}\n{publisher}"

        return answer
    
    #Actual Algorithm goes here:

    def groupbynumones(self) -> bool:
        """
        Step 1:
            Group All the minterms (and possibly Maxterms) by ammount of change in their Binary Representation.
        """
        NumInputVars = self.NumInputVars 

        unsortedBinaryTerms = []

        if self.MinorMax == "minterms":
            # Combine minterms and dont cares into one list
            all_terms = self.Minterms + self.DontCares
        elif self.MinorMax == "Maxterms":
            # Combine minterms and dont cares into one list
            all_terms = self.Maxterms + self.DontCares

        # Sort the combined list
        sorted_terms = sorted(all_terms)

        # Convert sorted terms to binary and append to unsortedBinaryTerms
        for term in sorted_terms:
            decimal = convertdecimaltobinarywithzeros(term, NumInputVars)
            unsortedBinaryTerms.append(decimal)

        sortedBinaryTerms = sorted(unsortedBinaryTerms, key=lambda x: x.count('1'))

        #------------------------------------------------------------------------------------
        #convert each sorted binary number into a decimal number so i know which midterm i am working with
        sortedDecimalTerms = []

        for term in sortedBinaryTerms:
            DecimalTerm = convertbinarytodecimal(term)
            if DecimalTerm in self.Minterms:
                sortedDecimalTerms.append(f"m{DecimalTerm}")
            elif DecimalTerm in self.Maxterms:
                sortedDecimalTerms.append(f"M{DecimalTerm}")
            elif DecimalTerm in self.DontCares:
                sortedDecimalTerms.append(f"d{DecimalTerm}")

        #------------------------------------------------------------------------------------
        #as we append the data to the table we need to find out the groups to know which binary numbers to compare
            
        SQL = "INSERT INTO stl_matchedpairs1 (groupp, matched_pairs, bin_rep, checked) VALUES (?, ?, ?, ?)"
        
        for index in range(0, len(sortedDecimalTerms)):
            #data to insert
            datatoinsert = [(sortedBinaryTerms[index].count('1'),f"{sortedDecimalTerms[index]}",f"{sortedBinaryTerms[index]}",0)]

            #inserting data into the 'stl_matchedpairs1' table using placeholders
            self.cursor.executemany(SQL, datatoinsert)

        #------------------------------------------------------------------------------------

        return 0
    
    def findMatchedpairs(self, matchedpairstable:str="1") -> bool:
        """
        Step 2:
            Find Match Pairs by comparing EVERY minterm in a group with every other minterm in group +1 of that minterm.
            The Comparison must happen between the Binary Representation of one minterm and the next, though we only move them on to the next step-
            if they are different by one variable. We represent the different variable by an Underscore in place of the 0/1.

            do this step over asmany times as many time as needed to find all possible matched pairs.
        """

        #------------------------------------------------------------------------------------
        #groupp in table we are currently working with
        grouppnum = 0

        #find largest groupp num in the given table
        self.cursor.execute(f"SELECT MAX(groupp) FROM stl_matchedpairs{matchedpairstable}")
        largestGrouppNum = (self.cursor.fetchall())[0][0]
        
        #Testing Purposes
        #print(f"The Largest Group in table number{matchedpairstable} = {largestGrouppNum}.\n")

        #Write some SQL to get all groups n (n meaning smallest group that we havent gotten yet)
        self.cursor.execute(f"SELECT * FROM stl_matchedpairs{matchedpairstable} WHERE groupp = {grouppnum}")
        matchinggroup = self.cursor.fetchall()

        for groupp in range(largestGrouppNum):
            #Write some SQL to get all groups n + 1 (to be compared to every group n)
            self.cursor.execute(f"SELECT * FROM stl_matchedpairs{matchedpairstable} WHERE groupp = {grouppnum + 1}")
            matchinggroupandone = self.cursor.fetchall()

            #Do that untill there is no n + 1 to compare against.
            #print(f"{matchinggroup} are compared against: {matchinggroupandone}")

            #for each comparison we are comparing the Binary Representation to find single digit changes,
            #if we manage to find these single digit changes append the difference to the SQl Table and change the changed bit to an underscore,
            #when something is found with a single bit change, we need to "check" every minterm involved so at the end we can figure out what has been used.

            #compare the two lists
            for grouppp in matchinggroup:
                for groupppp in matchinggroupandone:
                    
                    #takes two binary strings and compares them: EX: 0010 and 0000 = 00_0
                    differentbits = compareTwoBinaryStrings(grouppp[3],groupppp[3])

                    #print(f"{grouppp[3]} checked via: {groupppp[3]} = {differentbits} different bits")

                    #store the first and last numbers in a given set of minterms to make shure that we dont break the rule of:
                    """So, if you notice throughout all of the pairings, the right hand value is consistently at least larger than the left hand value

                    for example, (1,3), 3 is greater than 1, (3,7), 7 is greater than 3, (9,13), 13 is greater than 9

                    This same concept is carried over to pairs with two dashes or differing bits:

                    (1,3,9,11): 1 < 3 < 9 < 11
                    (2,3,10,11): 2 < 3 < 10 < 11
                    (3,7,11,15): 3 < 7 < 11 < 15

                    A pairing of (1,9,3,11) would break this rule: 1 < 9 !< 3 < 11"""

                    #should get the last bit involved in the first minterm
                    firstgrouplastbit = int(((grouppp[2]).replace('-',' ').replace('m','').replace('M','').replace('d','').split())[-1])
                    #should get the first bit involved in the first minterm
                    secondgroupfristbit = int(((groupppp[2]).replace('-',' ').replace('m','').replace('M','').replace('d','').split())[0])

                    if differentbits != "NA":
                        #---
                        #Append the data to the table
                        
                        SQL = f"INSERT INTO stl_matchedpairs{int(matchedpairstable)+1} (groupp, matched_pairs, bin_rep, checked) VALUES (?, ?, ?, ?)"
        
                        #data to insert
                        datatoinsert = [(differentbits.count('1'),f"{grouppp[2]}-{groupppp[2]}",f"{differentbits}",0)]

                        #i think that if i make an if statement that only appends stuff if the bit is bigger then we stay winning, but we have to check them off still? i think
                        if firstgrouplastbit < secondgroupfristbit:
                            #inserting data into the 'stl_matchedpairs1' table using placeholders
                            self.cursor.executemany(SQL, datatoinsert)

                        #--

                        #check off both groupps involved:
                        SQL1 = f"UPDATE stl_matchedpairs{matchedpairstable} SET checked = 1 WHERE matched_pairs = '{grouppp[2]}';"
                        SQL2 = f"UPDATE stl_matchedpairs{matchedpairstable} SET checked = 1 WHERE matched_pairs = '{groupppp[2]}';"

                        #TELLS programmer what the sql is, also tells me that the execute command is being used way to much
                        SQL3 = f"{SQL1}\n{SQL2}"
                        #print(SQL3)

                        self.cursor.executescript(SQL3)
                                
                        #---

            #so that i dont have to do another SQL query i will be setting the old n+1 to the new n
            matchinggroup = matchinggroupandone
            grouppnum += 1

        #------------------------------------------------------------------------------------

        #determine if we need to call this function again using the ammount of matched pairs in this table
        self.cursor.execute(f"SELECT COUNT(*) FROM stl_matchedpairs{int(matchedpairstable)+1}")
        ammountofmatchedpairs = (self.cursor.fetchall())[0][0]
        if ammountofmatchedpairs > 0:
            self.findMatchedpairs(int(matchedpairstable)+1)

        return 0
    
    
    def primeimplicantstable(self) -> bool:
        """
        Step 4:
            After all matched pairs/Prime implicants are found we need to make a new table called the Prime Implicant Table:
            This table has one purpose, make it obious which minterms used in a prime implicant show up only once. If If there is a pair of two-
            that only show up once we write down the Prime Implicants in the ouput function and go find if there are any more. If there arnt we have our answer.

            I want it to be said that you can use SQL to check if a column has a number for example query the matched_pairs_involved table with "m52" and you will get one of the results with that in it!
        """

        chosenPrimeImplicants = []
        primeImplicants = []
        mintermsinvolved = []

        for counter in range(6):
            #Fetch all records from the first matched pairs table
            self.cursor.execute(f"Select * FROM stl_matchedpairs{counter+1} WHERE checked = 0")
            Matchedpairdata = self.cursor.fetchall()

            #make shure there is something in side of the Matchedpairtable
            if Matchedpairdata != []:
                #check every pair in the current table
                for matchedpair in Matchedpairdata:
                    #Check if the binrep of the prime implicant has allready been taken
                    if matchedpair[3] not in chosenPrimeImplicants:
                        mintermsinvolved.append(matchedpair[2])

                        #if it hasnt append the implicant to a register of all know implicants
                        chosenPrimeImplicants.append(matchedpair[3])

                        #find what that equles in input terms
                        primeImplicants.append(bintoinputvars(matchedpair[3], self.ValidInputChars))
                        
        #print(primeImplicants)
        #print(mintermsinvolved)
        
        #append all the new data to a long SQL statement to append it to the primeimplicants table
        #stl_primeimplicanttable(pk_id INTEGER PRIMARY KEY,prime_implicants TEXT,{termforinput})

        #This Piece of shit (lol) literaly just takes a string "m1-m3-m5-m3" and converts it into a list [[m1,m3,m5,m3]]
        for index in range(0, len(mintermsinvolved)):
            #setup variables
            mintermsql = ", "
            mintermsqldata = [1]
            mintermsqlquestions = "?"
            dontcare = False
            lastchar = ''

            #for each char in a string ex: "m1-m3-m5-m3"
            for character in mintermsinvolved[index]:
                #if the char is a dont care dont append anything untill the char we are working with is not a dont care
                if character == 'd':
                    dontcare = True
                    if lastchar == '-':
                        #if the last char was a '-' then we have to take of some bad data that should have been here in the first place
                        mintermsqldata.remove(1)
                        mintermsql = mintermsql[:-2]
                        mintermsqlquestions = mintermsqlquestions[:-3]
                    elif lastchar == '':
                        mintermsqldata.remove(1)
                        mintermsql = mintermsql[:-2]
                        mintermsqlquestions = mintermsqlquestions[:-1]

                elif character == '-':
                    #if the char is a '-' append that data needed to seperate this term from the last one
                    mintermsql += ", "
                    mintermsqldata.append(1)
                    if mintermsqlquestions == '':
                        mintermsqlquestions += "?"
                    else:
                        mintermsqlquestions += ", ?"
                    

                elif ((character == 'm' or character == 'M') and (dontcare == True)):
                    #cherck if current answer is a dont care and if it is not dont care is true
                    dontcare = False
                    mintermsql += character

                else:
                    #if none of that stuff is true append the char to the working data
                    if dontcare == False:
                        mintermsql += character

                lastchar = character
            
            if mintermsqldata != []:

                SQL = f"""INSERT INTO stl_primeimplicanttable (prime_implicants,matched_pairs_involved{mintermsql}) VALUES ("{primeImplicants[index]}","{mintermsinvolved[index]}", {mintermsqlquestions})"""

                """print(f"{SQL}")
                print("\n")"""
                self.cursor.executemany(SQL, [mintermsqldata])
        #---
        
        self.connection.commit()

        #check every column of of the implicants table to find the columns where there is only one 1 then append them to the list
        #if we are solving for max terms is this still correct?----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        onlyone = []
        onlyonetermsinvolved = []
        for minterm in self.Minterms:
            SQL = f"""SELECT * FROM stl_primeimplicanttable WHERE m{minterm} = 1"""
            self.cursor.execute(SQL)
            result = self.cursor.fetchall()
            if len(result) == 1:
                if result[0][1] not in onlyone:
                    onlyone.append(result[0][1])
                    onlyonetermsinvolved.append(result[0][2])


        #Take the lists of onlyones and search it to see if there are any minterms missing from all the functions
        #if there is then we need to make that happen mimimally.
        #print(onlyonetermsinvolved)

        #all numbers involved just numbers
        justnumbersinvolved = []
        
        #iterate though every term in the terms involved.
        for terminvolved in onlyonetermsinvolved:
            #Get rid of the decorative m's
            terminvolved = terminvolved.replace("m","")
            terminvolved = terminvolved.replace("M","")

            #remove all the terms that begin with d until the - or end
            terminvolved += "-"
            def delete_between(string, start, end):
                """Deletes everything between the start and end characters in a string."""
                newstring = ""
                doappend = True

                #go though each char in the string and if it is the starting char stop appending the string to the output, if it is the ending char start appending to the output
                for i in range(0,len(string)):
                    if string[i] == start:
                        doappend = False
                    if doappend == True:
                        newstring += string[i]
                    if string[i] == end:
                        doappend = True

                #if at the end there is still a thing you want gon from the end remove it
                if newstring[-1] == end:
                    newstring = newstring[:-1]

                return newstring
            
            #print("1",terminvolved)
            terminvolved = delete_between(terminvolved,"d","-")
            #print("2",terminvolved)
            #print("\n")


            #Get len of terminvolved
            lenterminvolved = len(terminvolved)
            #Create a variable to store the current number in the terms involved
            numberstr = ""
            #keep track of all numbers 
            numbers = []
            #iterate through every value of the term involved
            for index in range(0,lenterminvolved):
                if terminvolved[index] == "-":
                    #Convert numberstr into a int
                    number = int(numberstr)
                    numbers.append(number)

                    #reset the numberstr to get ready for the next number     
                    numberstr = ""
                else:
                    #add the current char to the string to be converted into a number
                    numberstr += terminvolved[index]

                    if lenterminvolved == index+1:
                        #Convert numberstr into a int
                        number = int(numberstr)
                        numbers.append(number)

            justnumbersinvolved.append(numbers)

        #compare if the list of rangeonlyonetermsinvolved includes atleast one of each minterm in the input function to make shure we dont have any not covered
        #self.Minterms
        
        #list to store the minterms missing
        termsnotyetintegrated = []

        for term in self.Minterms:
            inside = False
            for numberss in justnumbersinvolved:
                if term in numberss:
                    #if this passes even once somewhere is that minterm in the list
                    inside = True
            #after all the current numbersinvolved have been compared against the minterms given at the start we can
            #decide what was some how left out, i dont know why this is...
            if inside == False:
                if term not in termsnotyetintegrated:
                    termsnotyetintegrated.append(term)
                
        #print(termsnotyetintegrated)


        #list of all possibly needed to add additional matched pairs.
        #there are two of them because if i get less matches running from a different side then that side is more minimal!
        additionalmatchedpairsleft = []
        additionalmatchedpairsright = []

        #1
        #check every column of of the implicants AGAIN table to add the ones that were missed then append them to the list
        for minterm in termsnotyetintegrated:
            SQL = f"""SELECT * FROM stl_primeimplicanttable WHERE m{minterm} = 1"""
            self.cursor.execute(SQL)
            result = self.cursor.fetchall()

            if result[0][1] not in additionalmatchedpairsleft:
                additionalmatchedpairsleft.append(result[0][1])  

        #2
        #check every column of of the implicants AGAIN table to add the ones that were missed then append them to the list
        for minterm in reversed(termsnotyetintegrated):
            SQL = f"""SELECT * FROM stl_primeimplicanttable WHERE m{minterm} = 1"""
            self.cursor.execute(SQL)
            result = self.cursor.fetchall()

            if result[0][1] not in additionalmatchedpairsright:
                additionalmatchedpairsright.append(result[0][1])  

        lenadditionalleft = len(additionalmatchedpairsleft)
        lenadditionalright = len(additionalmatchedpairsright)

        #print(additionalmatchedpairsleft, lenadditionalleft)

        #print(additionalmatchedpairsright, lenadditionalright)
        
        #check which way has less terms then output that one
        if lenadditionalleft <= lenadditionalright:
            for term in additionalmatchedpairsleft:
                onlyone.append(term)
        else:
            for term in additionalmatchedpairsright:
                onlyone.append(term)

        #Take the list of answers and put them in the correct format
        self.answer = "F = "
        howmanyones = len(onlyone)
        for one in onlyone:
            self.answer += f"{one}"
            if howmanyones > 1:
                self.answer += " + "
            howmanyones -= 1

        #Make shure the program actually writes to the disk
        self.connection.commit()

        #If you where to print the answer you would be done!
        return 0

    def calculateanswer(self) -> bool:
        """Essentially runs all the step functions to calculate the final answer, It is possible to calculate the answer step by step by putting in the functions one by one:
        1. self.TruthTableDataIntoTruthTable() -- Make shure input is in correct format
        2. self.groupbynumones() -- Make first table grouped by ones
        3. self.findMatchedpairs() -- Find matched pairs using first table
        4. self.primeimplicantstable() -- find prime implicants using matched pairs tables
        """
        #make shure all input functions are in the correrct format
        #print(f"Function taken as input: {self.TruthTableDataIntoTruthTable()}")

        #Solve the problem
        self.groupbynumones()

        self.findMatchedpairs()

        self.primeimplicantstable()

        return 0
    

#This is a useful function for the object, I dont know how many times im going to need to call it

def convertdecimaltobinarywithzeros(tobebinary:int, sizeofbiggestnum:int=0) -> str:
    """takes a number and converts it to binary, such as 3 -> 11.
        if given a seccond argument that is larger than the result of the first binary number it will add zeros the the front of the number
    """
    result = format(tobebinary, 'b')

    #add the correct number of zeros the the binary number
    while len(result) < sizeofbiggestnum:
        result = f"0{result}"

    return result

def convertbinarytodecimal(tobedecimal:str) -> int:
    """Function takes in a number '01011' and converts it into decimal, 11"""
    bin = 0
    counter = len(tobedecimal)-1

    for onepiece in tobedecimal:
        bin += (int(onepiece)*(2**counter))
        counter -= 1
    #term(binary) = rm(decimal) 
    return bin

def compareTwoBinaryStrings(bin1:str, bin2:str) -> str:
    """Takes two Binary Strings '0010' and '0000 returns the difference if only one var changed
        EX: 0010 and 0000 = 00_0
        EX: 10_0 and 10_1 = 10__
        EX: _001 and _000 = _00_

        EX: 1001 and 0100 = NA
    """
    answer = ""
    numBitsDifferent = 0
    #Checks ever bit against the opposing bit and if they are equle it outputs the same bit
    for bin in range(len(bin1)):
        if bin1[bin] == bin2[bin]:
            answer += f"{bin1[bin]}"
        elif numBitsDifferent < 1:
            numBitsDifferent += 1
            answer += "_"
        else:
            return "NA"
    return answer

def bintoinputvars(binary:str, ValidInputs:list) -> str:
    """take a input: _0_1: and return B`D"""
    answer = ""
    
    counter = 0
    for bin in binary:
        
        if bin == '0':
            answer += f"{ValidInputs[counter]}'"
        elif bin == '1':
            answer += f"{ValidInputs[counter]}"

        counter += 1

    return answer
        
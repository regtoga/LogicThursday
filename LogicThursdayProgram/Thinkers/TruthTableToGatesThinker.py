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
        self.numbermatchedpairstables = 10

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

            #update the number of matched pairs tables using my own crude method... i just dont want to run out of space...
            self.numbermatchedpairstables = self.NumInputVars * 3

            #I think that dropping a table will clear it, so that is what this does
            tables = [f"stl_matchedpairs{i}" for i in range(1, self.numbermatchedpairstables+1)] + ["stl_primeimplicanttable"]
            SQL = "\n".join([f"DROP TABLE IF EXISTS {table};" for table in tables])


            #Run the SQL
            self.cursor.executescript(SQL)

            #----Create the table for when we group by number of 1's in the bin rep
            #The range of the number is the number of tables im generating for matched pairs
            i = 0
            while i in range(self.numbermatchedpairstables):
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
                tables = [f"stl_matchedpairs{i}" for i in range(1, self.numbermatchedpairstables+1)] + ["stl_primeimplicanttable"]
                SQL = "\n".join([f"DROP TABLE IF EXISTS {table};" for table in tables])

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

        for counter in range(self.numbermatchedpairstables):
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
        Group all minterms (and possibly maxterms) by the number of '1's in their binary representation.
        This function assumes that all minterms have been correctly derived from maxterms if necessary.
        """
        NumInputVars = self.NumInputVars 

        # Combine minterms and don't cares
        all_terms = self.Minterms + self.DontCares

        # Sort the combined list
        sorted_terms = sorted(all_terms)

        # Convert sorted terms to binary and append to a list
        binary_terms_with_groups = []
        for term in sorted_terms:
            binary_rep = convertdecimaltobinarywithzeros(term, NumInputVars)
            binary_terms_with_groups.append((binary_rep.count('1'), term, binary_rep))

        # Sort binary terms/groups by the number of '1's
        sorted_binary_terms = sorted(binary_terms_with_groups, key=lambda x: x[0])

        # Insert the sorted binary terms into the database table stl_matchedpairs1
        SQL = "INSERT INTO stl_matchedpairs1 (groupp, matched_pairs, bin_rep, checked) VALUES (?, ?, ?, ?)"
        data_to_insert = []

        for num_ones, term, bin_rep in sorted_binary_terms:
            # Determine the term label
            if term in self.Minterms:
                term_label = f"m{term}"
            elif term in self.DontCares:
                term_label = f"d{term}"
            else:
                # This case should not happen if everything is correctly set up
                continue

            # Prepare the data for insertion
            data_to_insert.append((num_ones, term_label, bin_rep, 0))

        # Execute the insert operation
        self.cursor.executemany(SQL, data_to_insert)
        self.connection.commit()

        return True
    
    def findMatchedpairs(self, matchedpairstable: str = "1") -> bool:
        """
        Step 2:
        Find matched pairs by comparing every term in a group with every term in the next group.
        The comparison occurs between binary representations, differing by exactly one bit.
        These pairs are then stored in a new table for the next round of comparisons.
        """

        # Get the largest group number in the current table
        self.cursor.execute(f"SELECT MAX(groupp) FROM stl_matchedpairs{matchedpairstable}")
        largestGrouppNum = self.cursor.fetchone()[0]

        if largestGrouppNum is None:
            return False  # Exit if there are no groups

        # Iterate through the group numbers to find matched pairs
        for group_num in range(largestGrouppNum):
            # Retrieve terms from the current group
            self.cursor.execute(f"SELECT * FROM stl_matchedpairs{matchedpairstable} WHERE groupp = {group_num}")
            current_group = self.cursor.fetchall()

            # Retrieve terms from the next group
            self.cursor.execute(f"SELECT * FROM stl_matchedpairs{matchedpairstable} WHERE groupp = {group_num + 1}")
            next_group = self.cursor.fetchall()

            # Compare terms in current group with those in the next group
            for term1 in current_group:
                for term2 in next_group:
                    # Compare the binary representations to find differences by exactly one bit
                    new_bin_rep = compareTwoBinaryStrings(term1[3], term2[3])
                    if new_bin_rep != "NA":
                        # Ensure pairs are recorded only if they meet the strict ordering rule
                        terms_involved1 = list(map(int, term1[2].replace('m', '').replace('M', '').replace('d', '').split('-')))
                        terms_involved2 = list(map(int, term2[2].replace('m', '').replace('M', '').replace('d', '').split('-')))

                        if terms_involved1[-1] < terms_involved2[0]:
                            # Insert into the next matched pairs table
                            SQL = f"INSERT INTO stl_matchedpairs{int(matchedpairstable)+1} (groupp, matched_pairs, bin_rep, checked) VALUES (?, ?, ?, ?)"
                            new_matched_pairs = f"{term1[2]}-{term2[2]}"
                            data_to_insert = (new_bin_rep.count('1'), new_matched_pairs, new_bin_rep, 0)
                            self.cursor.execute(SQL, data_to_insert)

                            # Mark the original terms as checked
                            self.cursor.execute(f"UPDATE stl_matchedpairs{matchedpairstable} SET checked = 1 WHERE PK_id = ?", (term1[0],))
                            self.cursor.execute(f"UPDATE stl_matchedpairs{matchedpairstable} SET checked = 1 WHERE PK_id = ?", (term2[0],))

        # Commit changes to the database
        self.connection.commit()

        # Determine if further steps are needed
        self.cursor.execute(f"SELECT COUNT(*) FROM stl_matchedpairs{int(matchedpairstable)+1}")
        number_of_matched_pairs = self.cursor.fetchone()[0]

        if number_of_matched_pairs > 0:
            # Call this function recursively if new pairs were found
            self.findMatchedpairs(str(int(matchedpairstable) + 1))

        return True
    
    
    def primeimplicantstable(self) -> bool:
        """
        Construct the prime implicant table and generate the minimized boolean expression
        using variable formats like 'A'B'C''.
        """

        # Collect unmatched terms (prime implicants) from all matched pairs tables
        prime_implicants = []

        for table_index in range(1, self.numbermatchedpairstables):
            # Fetch all unmatched entries
            self.cursor.execute(f"SELECT * FROM stl_matchedpairs{table_index} WHERE checked = 0")
            unmatched = self.cursor.fetchall()

            for term in unmatched:
                if term[3] not in {imp[0] for imp in prime_implicants}:
                    prime_implicants.append((term[3], term[2]))

        # Translate prime implicants to boolean expressions
        prime_expressions = [bintoinputvars(binary_rep, self.ValidInputChars) for binary_rep, _ in prime_implicants]

        # Determine term coverage
        term_coverage = {minterm: set() for minterm in self.Minterms}

        for expression, (_, terms) in zip(prime_expressions, prime_implicants):
            involved_terms = set(map(int, terms.replace('m', '').replace('d', '').split('-')))
            for minterm in involved_terms:
                if minterm in term_coverage:
                    term_coverage[minterm].add(expression)

        # Identify essential primes
        essential_expressions = {next(iter(exprs)) for exprs in term_coverage.values() if len(exprs) == 1}

        # Collect remaining prime expressions for further coverage
        covered = set(essential_expressions)
        uncovered_terms = {term for term, exprs in term_coverage.items() if not exprs.intersection(covered)}

        while uncovered_terms:
            previous_uncovered = uncovered_terms.copy()

            # Pick the expression covering the most uncovered terms
            candidate, adds_coverage = None, 0
            for expression, (_, terms) in zip(prime_expressions, prime_implicants):
                involved_terms = set(map(int, terms.replace('m', '').replace('d', '').split('-')))
                new_coverage = len(uncovered_terms.intersection(involved_terms))

                if new_coverage > adds_coverage:
                    candidate, adds_coverage = expression, new_coverage

            if candidate:
                covered.add(candidate)
                involved_terms = [term for term in term_coverage if candidate in term_coverage[term]]
                uncovered_terms.difference_update(involved_terms)

            # Break if no new terms are covered
            if previous_uncovered == uncovered_terms:
                break

        # Formulate the minimized expression
        if covered:
            self.answer = "F = " + " + ".join(sorted(covered))
        else:
            self.answer = "F = 1" if self.nummin > 0 else "F = 0"

        return True

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
        
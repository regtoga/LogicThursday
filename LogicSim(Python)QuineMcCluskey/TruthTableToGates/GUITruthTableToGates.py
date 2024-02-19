#This File should ONLY be the GUI the rest goes inside of the TruthTableToGates object

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
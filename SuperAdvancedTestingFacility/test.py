#remove all the terms that begin with d until the - or end
terminvolved = 'd0-2-4-d6-3-5-d7'
def delete_between(string, start, end):
    """Deletes everything between the start and end characters in a string."""
    newstring = ""
    doappend = True

    for i in range(0,len(string)):
        if string[i] == start:
            doappend = False
        if doappend == True:
            newstring += string[i]
        if string[i] == end:
            doappend = True

    if newstring[-1] == end:
        newstring = newstring[:-1]

    return newstring
terminvolved = delete_between(terminvolved,"d","-")
print(terminvolved)
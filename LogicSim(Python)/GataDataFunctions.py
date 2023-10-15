import GatesToTruthTableCLI as CLI
import GatesClass as gate

def PrintAllGateTypes() -> str:
    """Function that prints all hardcoded GateTypes"""
    outputstr = ""
    GateTypes = {
        0:"(0) Use your own gate \n",
        1:"(1) NOT \n",
        2:"(2) SevenSegdisplayDriver \n",
        3:"(3) AND \n",
        4:"(4) OR \n",
        5:"(5) NOR \n",
        6:"(6) NAND \n",
        7:"(7) XOR \n",
        8:"(8) ADDER: \n",
        9:"(9) TWOBITADDER \n",
        10:"(10) FOURBITADDER \n",
        11:"(11) EIGHTBITADDER \n",
        12:"(12) ALU \n"
    }

    for gate in range(0, len(GateTypes)):
        outputstr += f"{GateTypes.get(gate)}"
    
    print(outputstr)

def GateDimentionValuesfunction(intgatechosen:int) -> list:
    """Returns a predetermined imputmask unless user chooses something that isnt on the list, then they are 
    forced to make their own"""
    GateDimentionValues = {
        1:[[[0]],[[0]]],
        2:[[[0,0,0,0]],[[0],[0],[0],[0],[0],[0],[0],[0]]],
        3:[[[0],[0]],[[0]]],
        4:[[[0],[0]],[[0]]],
        5:[[[0],[0]],[[0]]],
        6:[[[0],[0]],[[0]]],
        7:[[[0],[0]],[[0]]],
        8:[[[0],[0],[0]],[[0],[0]]],
        9:[[[0,0],[0,0],[0]],[[0,0],[0]]],
        10:[[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0]]],
        11:[[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0]],[[0,0,0,0,0,0,0,0],[0]]],
        12:[[[0,0,0,0],[0,0,0,0],[0]],[[0,0,0,0],[0],[0],[0]]]
    }

    
    GateDimentions = GateDimentionValues.get(intgatechosen, f"{intgatechosen} did not correspond to a built in gate.")
    print(GateDimentions)
    if GateDimentions == f"{intgatechosen} did not correspond to a built in gate.":
        print("You must correct your actions by imputing your own gate mask!")
        GateDimentions = CLI.GetDimentionsOfGateCLI()
    return GateDimentions

def ChooseGateToUse(intgatechosen:int, combinations:list, num:int) -> list:
    """Using the integer provided by user to determine what gate to test, a list of inputs, and an index, 
    this function will return a single result"""

    if intgatechosen == 1:
        return [gate.NOT_GATE(combinations[num][0][0])]
    elif intgatechosen == 2:
        return gate.sevensegdisplaydriver(combinations[num][0])
    elif intgatechosen == 3:
        return [gate.AND_GATE(combinations[num][0][0],combinations[num][1][0])]
    elif intgatechosen == 4:
        return [gate.OR_GATE(combinations[num][0][0],combinations[num][1][0])]
    elif intgatechosen == 5:
        return [gate.NOR_GATE(combinations[num][0][0],combinations[num][1][0])]
    elif intgatechosen == 6:
        return [gate.NAND_GATE(combinations[num][0][0],combinations[num][1][0])]
    elif intgatechosen == 7:
        return [gate.XOR_GATE(combinations[num][0][0],combinations[num][1][0])]
    elif intgatechosen == 8:
        return (gate.ADDER(combinations[num][0][0],combinations[num][1][0],combinations[num][2][0]))
    elif intgatechosen == 9:
        return (gate.TWOBITADDER(combinations[num][0],combinations[num][1],combinations[num][2][0]))
    elif intgatechosen == 10:
        return (gate.FOURBITADDER(combinations[num][0],combinations[num][1],combinations[num][2][0]))
    elif intgatechosen == 11:
        return (gate.EIGHTBITADDER(combinations[num][0],combinations[num][1],combinations[num][2][0]))
    elif intgatechosen == 12:
        return (gate.ALU(combinations[num][0],combinations[num][1],combinations[num][2][0]))



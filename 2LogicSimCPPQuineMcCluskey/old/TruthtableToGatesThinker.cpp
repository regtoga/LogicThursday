#include <string>
#include <vector>

#include <time.h>

//If this file includes iostream when im done i am quitting my job
#include <iostream>

class BooleanList{
    public:
        //Adds a boolean value to the list.
        void add(bool value){
            list.push_back(value);
        }

        //Removes a boolean value from the list
        void remove(bool value){
            for (int i = 0; i < list.size(); i++){
                if (list[i] == value){
                    list.erase(list.begin() + i);
                    break;
                }
            }
        }

        //returns the boolean value at the specified index.
        bool get(int index){
            return list[index];
        }

        //Returns the size of the list.
        int size(){
            return list.size();
        }
    
    private:
        std::vector<bool> list;
};

//Create prototypes for easy calling
bool NOT(bool input);
bool AND(bool input1, bool input2);
bool OR(bool input1, bool inpu2);

bool calculateFunctionOutput(std::string function, std::vector<bool> inputs);

class TruthTableToGates{
    private:
        //min var to which everything will be derived.
        std::string functionToSolve = "";
        std::string justfunction = "";
        //Create two lists for minterms, and maxterms
        std::vector<int> minterms;
        int nummin = 0;
        std::vector<int> maxterms;
        int nummax = 0;
        std::string databasename = "";

        //answer vars, currently arnt used in the original program but they could be
        std::string TruthTable = "";
        std::string AnswerFunction = "";

        int largestvarnum = 0;
        //Im deprecating just function in english
        const char ValidInputChars[52] = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};

    public:

        //Default Constructor
        TruthTableToGates(std::string function){
            functionToSolve = function;

            //Create vars
            bool startapending = true;
            bool isFfound = false;
            int leninput = functionToSolve.length();
            char currentchar;

            int lenjustfunction;

            for (int index = 0; index < leninput; index++){
                //this is the variable for the current char
                currentchar = functionToSolve[index];
                
                if ((tolower(currentchar) == 'f') && (isFfound == false)){
                    startapending = false;
                    isFfound = true;
                }

                //if all conditions pass start
                if ((startapending == true)&&(currentchar != ' ')){
                    justfunction += currentchar;
                }

                if (currentchar == '='){
                    startapending = true;
                }
            }

            //Its possible that at this point i will need to remove all spaces from the output string
            //Its just that from what i can tell it alrady does that?
            
            //Create the database name based off the input function
            if (justfunction.length() < 10){
                databasename = justfunction + ".db";
            }else{
                for (int index = 0; index < 10; index++){
                    databasename += justfunction[index];
                }
                databasename +=".db";
            }

            //Take the justfunction of the input and find the largest var it uses, such as A'BCE = E -> the num of inputs is 5
            
            lenjustfunction = justfunction.length();

            for (int index = 0; index < lenjustfunction; index++){

                for (int index2 = 0; index2 < 42; index2++){
                    if (justfunction[index]==ValidInputChars[index2]){
                        largestvarnum = index2;
                    }
                }
            }
            
            //std::cout << "The number " << largestvarnum << " ='s " << ValidInputChars[largestvarnum] << std::endl
            //create a list of bools that will be counted to provide the TruthTable
            std::vector<bool> inputslist = {false};
            int termnum = -1;
            bool runOne = true;

            bool allaretrue = false;

            int binarycountingindex = largestvarnum;
            bool currentlistvalue;

            while(allaretrue==false){
                termnum++;

                for (int index = 0; index <= largestvarnum; index++){
                    allaretrue = true;
                    if (inputslist[index] == false){
                        allaretrue = false;
                        break;
                    }
                }
                //on first run clear the inputslist then put the correct number of termsinto it
                if (runOne == true){
                    inputslist = {};

                    for (int index = 0; index <= largestvarnum; index++){
                        inputslist.push_back(false);
                    }

                    runOne = false;
                }else{
                    //may cause issues.
                    if (allaretrue == true){
                        break;
                    }
                    //#make a recursive function to do counting
                    //This is my binaryCountingWithList() function
                    binarycountingindex = largestvarnum;
                    while (binarycountingindex >= 0){
                        currentlistvalue = inputslist[binarycountingindex];
                        if (currentlistvalue != true){
                            inputslist[binarycountingindex] = NOT(currentlistvalue);
                            break;
                        }
                        inputslist[binarycountingindex] = NOT(currentlistvalue);
                        binarycountingindex--;
                    }
                }

                //Do calculation
                bool functionoutput = calculateFunctionOutput(justfunction, inputslist);
                
                if (functionoutput == false){
                    maxterms.push_back(termnum);
                    nummax++;
                }else{
                    minterms.push_back(termnum);
                    nummin++;
                }
            }
        }

        //Getters
        std::string get_databaseName(){
            return databasename;
        }

        std::string get_functionToSolve(){
            return functionToSolve;
        }

        std::string get_TruthTable(){
            return TruthTable;
        }

        std::string get_AnswerFunction(){
            return AnswerFunction;
        }

        std::string get_minterms(){
            std::string output = "";
            for (int index = 0; index < nummin; index++){
                output += std::to_string(minterms[index]);
                if (index + 1 != nummin){
                    output += ", ";
                }
            }
            return output;
        }

};

//Nessesary Binary functions = AND, OR, NOT
bool NOT(bool input){
    return !input;
}

bool AND(bool input1, bool input2){
    return input1 && input2;
}

bool OR(bool input1, bool input2){
    return input1 || input2;
}

int indexCPP(std::vector<char> list, char input){
    for (int index = 0; index < 52; index++){
        if (list[index] == input){
            return index;
        }
    }
    return -1;
}

//calculateFunctionOutput goes here
//"""This function takes a function input such as A'BCD+AB'C' and an input and outputs the result """

//I also dont quite know how to do this function because its seccond input is a list aswell
bool calculateFunctionOutput(std::string function, std::vector<bool> inputs){
    //"""This function takes a function input such as A'BCD+AB'C' and an input and outputs the result """
    std::vector<char> ValidInputChars = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};
    int answer = 0;
    bool num;
    std::vector<bool> oldanswers;
    int oldanswerlen = 0;
    
    bool firstNumInSequence = true;
    for (int index = 0; index < function.length(); index++){
        //check if current index is a ' or a + if it is and the last input was a ' append the current answer to the queue
        if ((function[index] == '\'') || (function[index] == '+')){
            if (function[index] == '+'){
                firstNumInSequence = true;
                if (function[index-1] == '\''){
                    oldanswers.push_back(answer);
                    answer = 0;
                    oldanswerlen++;
                }
            }
        }else{
            num = inputs[indexCPP(ValidInputChars, function[index])];

            //NOT opperation leading into an AND opperation of function[index1]
            if ((index+1 < function.length())&&(function[index+1] == '\'')){
                if (firstNumInSequence == true){
                    answer = NOT(num);
                    firstNumInSequence = false;
                }else{
                    answer = AND(NOT(num), answer);
                }
            }

            //AND opperation when at the end of a group of numbers
            else if ((index+1 < function.length())&&(function[index+1] == '+')){
                if (firstNumInSequence == true){
                    oldanswers.push_back(num);
                    firstNumInSequence = false;
                    oldanswerlen++;
                }else{
                    oldanswers.push_back(AND(num, answer));
                    oldanswerlen++;
                }
                answer = 0;
            }

            //AND opperation on the numbers
            else{
                if (firstNumInSequence == true){
                    answer = num;
                    firstNumInSequence = false;
                }else{
                    answer = AND(num, answer);
                }
            }
        }
    }

    //add the last answer to the old answers list
    oldanswers.push_back(answer);
    answer = 0;
    oldanswerlen++;

    //Take the list of answers and OR them together
    for (int index = 0; index < oldanswerlen; index++){
        if (oldanswers[index] == true){
            return true;
        }
    }

    return false;
}

int main(){
    //start timer
    clock_t start_time = clock();

    std::cout << "\nTest 1:" << std::endl;
    TruthTableToGates TToG("F = A'B + AB'C'");
    //std::cout << TToG.get_minterms() << std::endl;
    
    std::cout << "\nTest 2:" << std::endl;
    TruthTableToGates TToG2("F = A'B'C + BC'D' + A'CD + B'C'D");
    //std::cout << TToG2.get_minterms() << std::endl;

    std::cout << "\nTest 3:" << std::endl;
    TruthTableToGates TToG3("F = AB'C'DEF'G + A'B'C'D'E'FG' + A'B'C'D'E'F'G");
    //std::cout << TToG3.get_minterms() << std::endl;

    std::cout << "\nTest 4:" << std::endl;
    TruthTableToGates TToG4("F = A'B'C'D'E'F'Z");

    //std::cout << "\nTest 5:" << std::endl;
    //TruthTableToGates TToG5("F = a'");

    //stop timer
    clock_t end_time = clock();
    double duration = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    std::cout << "It took " << duration << " secconds!" << std::endl;
}



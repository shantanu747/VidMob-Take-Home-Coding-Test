'''
@Author: Shantanu Patil
VidMob Take-Home Exam
'''


'''
Function checks whether supplied string is a number by trying to typecast to float
Raises ValueError if typecast fails

@Params:
inp [str] - the char(s) you want to check if is a number

@Returns:
bool
''' 
def is_a_num(inp):
    try:
        float(inp)
        return True
    except ValueError:
        return False

'''
Function takes two numbers and and an operation and performs operation
For division, checks if user is trying to divide by zero - raises exception if so

@Params:
num1 [str] - the first number 
num2 [str] - the second number
operation [str] - operations to perform

@Returns
string representation of result to be added to expression list again 
'''
def perform_operation(num1, operation, num2):
    if(operation == "*"):
        return str(float(num1) * float(num2))
    elif(operation == "/"):
        if(float(num2) == 0.0):
            print("Division by zero not allowed here!")
            return
        return str(float(num1) / float(num2))
    elif(operation == "+"):
        return str(float(num1) + float(num2))
    elif(operation == "-"):
        return str(float(num1) - float(num2))
    else:
        #Unsupported operation - exit out
        print("Invalid operation provided, please try again")
        return

'''
Function checks user provided expression for invalid characters or invalid expression
Formats expression for easier evaluation  
Returns list with numbers and operations ready for evaluation by evaluate_expression()

@Params:
inputString [str]: expression provided by user

@Returns:
expression_list [List[str]]
'''
def setup_expression(inputString):
    #Used for pattern matching of string chars
    valid_chars = '0123456789().*/+-'
    operators = '*/+-'
    neg_number_prefixes = ['-.', '-0.']

    #Validate expression first
    # Check for any invalid chars in string or illegal repeating operators
    operators_in_series = 0 
    for char in inputString:
        if(char not in valid_chars):
            print("Invalid Input")
            print("Expression can only contain symbols for math operators(*, /, +, -) and numbers (0-9)")
            return
        if(char in operators):
            operators_in_series += 1
            if((operators_in_series == 2 and char != '-') or (operators_in_series > 2)):
                print("Syntax Error - cannot have more than 2 operators in a row and second operator must be \'-\'")
                return
        elif(operators_in_series > 0):
            #reset it back to 0 if operator series has been broken
            operators_in_series = 0

    #Initialize list with every character in expression
    expression_list = [char for char in inputString]

    index = 0
    #Combines individual digits into actual numbers 
    while(index < (len(expression_list) - 1)):
        if(is_a_num(expression_list[index]) and expression_list[index + 1] == "("):
            #The program does not support implicit multiplication - need operator between number and parentheses
            print("Invalid Input")
            print ("Expression cannot have parentheses directly after number - must be operator in between")
            return
        if(is_a_num(expression_list[index]) and is_a_num(expression_list[index + 1])):
            expression_list[index] += expression_list[index + 1]
            del expression_list[index + 1]
        elif(is_a_num(expression_list[index]) and expression_list[index + 1] == "."):
            if is_a_num(expression_list[index + 2]):
                expression_list[index] += expression_list[index + 1] + expression_list[index + 2]
                del expression_list[index + 2]
                del expression_list[index + 1]
            else:
                #dangling decimal, can safely ignore it
                del expression_list[index + 1]
        
        #Handles negative integers and negative decimals
        elif(expression_list[index] == '-'):
            if(index == 0 and (expression_list[index+1] == '.' or is_a_num(expression_list[index+1]))):
                #first number is negative - merge with next char
                expression_list[index] += expression_list[index + 1]
                del expression_list[index + 1]
            elif(expression_list[index-1] in operators and (expression_list[index+1] == '.' or is_a_num(expression_list[index+1]))):
                #confirm this is a second '-' char and thus this is part of another negative number and not meant as subtraction operator
                expression_list[index] += expression_list[index + 1]
                del expression_list[index + 1]
            else:
                #This fixes the issue of negative numbers not working
                expression_list.insert(index, '+')
                index += 1
        elif(expression_list[index] in neg_number_prefixes and is_a_num(expression_list[index+1])):
            expression_list[index] += expression_list[index + 1]
            del expression_list[index + 1]
        #Handle decimals
        elif(expression_list[index] == '.' and is_a_num(expression_list[index+1])):
            expression_list[index] += expression_list[index + 1]
            del expression_list[index + 1]
        else:
            index += 1
    return expression_list

'''
Driver function to evaluate expression. Receives user provided expression from main
Sets up expression by first calling setup_expression()
Solves expression: first solving parentheses, then multiplication/divison
Finally solves addition/subtraction and returns result
'''
def evaluate_expression(command_line_expression):
    expression = setup_expression(command_line_expression)
    if(not expression):
        return
    if(expression[0] == '(' and expression[-1] == ')'):
        del expression[-1]
        del expression[0]
    Parentheses = '()'

    parentheses_solved = False

    #If the length of the list is 1, there is only 1 number, meaning an answer has been reached.
    while len(expression) != 1:
        #If single number inside parentheses then no operations needed, strip parentheses
        #Assumption: operations inside parentheses have already been evaluated in a previous pass
        while(not parentheses_solved):
            index = 0
            if('(' not in expression and ')' not in expression):
                parentheses_solved = True
                break
            while(index < len(expression)-1):
                if(expression[index] == "(" and expression[index+2] == ")"):
                    del expression[index + 2]
                    del expression[index]
                else:
                    index += 1
            index = 0
            while(index < len(expression) - 1):
                if(expression[index] in "*/" and not (expression[index+1] in Parentheses or expression[index-1] in Parentheses)):
                    expression[index - 1] = perform_operation(expression[index - 1], expression[index], expression[index + 1])
                    del expression[index + 1]
                    del expression[index]
                    index = 0
                else:
                    index += 1
            #Handle add/subtract ops next
            index = 0
            while(index < len(expression) - 1):
                if(expression[index] in "+-" and not (expression[index+1] in Parentheses or expression[index-1] in Parentheses)):
                    expression[index - 1] = perform_operation(expression[index - 1], expression[index], expression[index + 1])
                    del expression[index + 1]
                    del expression[index]
                    index = 0
                else:
                    index += 1
        #Handle multiply/divide ops next
        index = 0
        while(index < len(expression) - 1):
            if(expression[index] in "*/" and not (expression[index+1] in Parentheses or expression[index-1] in Parentheses)):
                expression[index - 1] = perform_operation(expression[index - 1], expression[index], expression[index + 1])
                del expression[index + 1]
                del expression[index]
                index = 0
            else:
                index += 1
        #Handle add/subtract ops next
        index = 0
        while(index < len(expression) - 1):
            if(expression[index] in "+-" and not (expression[index+1] in Parentheses or expression[index-1] in Parentheses)):
                expression[index - 1] = perform_operation(expression[index - 1], expression[index], expression[index + 1])
                del expression[index + 1]
                del expression[index]
                index = 0
            else:
                index += 1
    return (float(expression[0]))


def main():
    wrong_counter = 0
    
    #Welcome message and inform user on how to use this program
    print("Welcome to the calculator by Shantanu Patil!\n")
    print("For calculations, enter command using \"calculate _expression_\" followed by the \"Enter\" or \"Return\" key.\n")
    print("For example, if you want to evaluate \"2+2\" then type in \"calculate 2+2\" in the command line and hit enter.\n")
    print("When finished type \"Done\" to exit the program. Note: none of these commands are case sensitive\n")
    print("If an invalid command is given more than 3 times in a row, the program will terminate\n")

    #Run while loop for as long as user gives correct command for evaluations
    #If user enters "Done" or enters invalid command more than 3 times, exit out of while loop and terminate program
    while(1):
        userInput = input("Please enter command: ")
        userInput = userInput.strip().split(" ")
        if(userInput[0].lower() == "calculate"):
            wrong_counter = 0 #set this counter back to 0 if it wasn't already
            expression = "".join(userInput[1:]) #this handles expressions separated by space e.g. '2 + 2'
            expression = expression.replace(" ", "") #for larger spaces in expression
            answer = evaluate_expression(expression)
            #If one of the functions did not return out early (returned NULL) print the answer
            if(answer is not None):
                print(answer)
        elif(userInput[0].lower() == "done"):
            wrong_counter = 0 #set this counter back to 0 if it wasn't already
            print("Done command received - exiting the program\n")
            return 0
        else:
            wrong_counter += 1
            if(wrong_counter == 3):
                print("Too many invalid commands - exiting program.")
                return 1
            #Print descriptive error message for user in case they made a typo
            print("Invalid command! Use \"calculate\" command with valid math expression to evaluate, or \"Done\" to close program.\n")
    

if __name__ == "__main__":
    #TODO: Nested parentheses need work - PEMDAS doesn't work as intended when nesting is involved
    main()


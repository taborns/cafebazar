def result(first_number, operator, second_number):
    if (operator == "+"):
        return first_number + second_number
    elif (operator == "-"):
        return first_number - second_number
    elif (operator =="*"):
        return first_number * second_number
    elif (operator =="/"):
        return first_number / second_number
    else:
        print ("please enter an appropriate operator")
        
def arthematic_operation():

    while (1):
        first_number = eval(input("Enter the first number"))
        operator = input("input an operator:")
        second_number = eval(input("Enter the second number"))
        first_number = float(result(first_number, operator, second_number))
        print(first_number)
        
        while (2):
            operator = input ("operator: ")
            second_number = eval(input("Enter another number"))
            first_number = result(first_number, operator, second_number)
            print(first_number)

arthematic_operation()
from colorama import Fore, Back, Style

def prRed(skk): 
    print("\033[91m {}\033[00m".format(skk))
def prGreen(skk):
    print("\033[92m {}\033[00m".format(skk))
def prYellow(skk):
    print("\033[93m {}\033[00m".format(skk))
def prLightPurple(skk):
    print("\033[94m {}\033[00m".format(skk))
def prPurple(skk):
    print("\033[95m {}\033[00m".format(skk))
def prCyan(skk):
    print("\033[96m {}\033[00m".format(skk))
def prLightGray(skk):
    print("\033[97m {}\033[00m".format(skk))
def prBlack(skk):
    print("\033[98m {}\033[00m".format(skk))


current_state = []
planning_stack = []
 # stack required in goal stack planning (only going to add sub goals)


def convert_list(list):
    temp = "".join((item + " | ") for item in list)
    return str(temp)


# Effects of action
# Predicates are added or removed from current state depending on the action being taken

#stack(X,Y) operation:
#adds: on X Y,clear X and arm_empty predicates to the planning_stack list
#removes: holding X and clear Y predicates from the current_state list
def stack(X, Y):
    current_state.append("on " + str(X) + " " + str(Y))
    current_state.append("clear " + str(X))
    current_state.append("arm_empty")
    current_state.remove("holding " + str(X))
    current_state.remove("clear " + str(Y))

#unstack(X,Y) operation:
#adds: holding X,clear X predicates to the planning_stack list
#removes: on X,Y,clear X and arm_empty predicates from the current_state list
def unstack(X, Y):
    current_state.append("holding " + str(X))
    current_state.append("clear " + str(Y))
    current_state.remove("on " + str(X) + " " + str(Y))
    current_state.remove("clear " + str(X))
    current_state.remove("arm_empty")

#pickup(X) operation:
#adds: holding X predicate to the planning_stack list
#removes: arm_empty, on_table X and clear X predicates from the current_state list
def pickup(X):
    current_state.append("holding " + str(X))
    current_state.remove("arm_empty")
    current_state.remove("on_table " + str(X))
    current_state.remove("clear " + str(X))

#putdown(X) operation:
#adds: arm_empty, on_table X and clear X predicates to the planning_stack list
#removes: holding X predicate from the current_state list
def putdown(X):
    current_state.append("arm_empty")
    current_state.append("on_table " + str(X))
    current_state.append("clear " + str(X))
    current_state.remove("holding " + str(X))


# Corresponding action and their preconditions required to satisfy the predicates are added to the planning_stack list

#To statisfy on(X,Y) predicate we need to execute a stack(X,Y) operation which has two preconditions i.e. holding(X) and clear(Y).
#These are all added to the planning_stack list.
def on(X, Y):
    planning_stack.append("stack " + str(X) + " " + str(Y))
    planning_stack.append("holding " + str(X))
    planning_stack.append("clear " + str(Y))

#To statisfy on_table(X) predicate we need to execute a 
#putdown(X) operation which has on3 precondition i.e. holding(X).
#These are all added to the planning_stack list.
def on_table(X):
    planning_stack.append("putdown " + str(X))
    planning_stack.append("holding " + str(X))

"""To statisfy clear(X) predicate we need to execute an unstack(Y,X) operation which has three preconditions i.e. arm_empty,on(Y,X) and clear(Y).
These are all added to the planning_stack list.
We have also taken care of the case where the program could not resolve solving the clear predicate when the block was already being held."""
def clear(X):

    check ="holding " + str(X)

    if check in current_state:
        planning_stack.append("putdown " + str(X))
    else:

        # Finding the block which is stacked on X
        check = "on "
        for predicate in current_state:
            if check in predicate:
                temp_list = predicate.split()

                if temp_list[2] == X:
                    break

        Y = str(temp_list[1])

      # Appending Unstack operation with its preconditions
        planning_stack.append("unstack " + str(Y) + " " + str(X))
        planning_stack.append("arm_empty")
        planning_stack.append("on " + str(Y) + " " + str(X))
        planning_stack.append("clear " + str(Y))

"""To statisfy holding(X) predicate we need to check whether the block X is on table or if it is on top of another block.
If the block is on table we execute the pickup(X) operation and its three preconditions i.e. arm_empty,on_table (X) and clear (X) are all added to the planning_stack list.

If block X is not on the table then we execute unstack(X,Y) operation and its three preconditions i.e. arm_empty,on (X,Y) and clear (X) are all added to the planning_stack list."""

def holding(X):  # sourcery skip: hoist-statement-from-if
    check = "on_table " + str(X)

    if check in current_state:
        planning_stack.append("pickup " + str(X))
        planning_stack.append("arm_empty")
        planning_stack.append("on_table " + str(X))
        planning_stack.append("clear " + str(X))

    else:
        # Finding the block on which X is stacked
        check = "on "

        for predicate in current_state:
            if check in predicate:
                temp_list = predicate.split()

                if temp_list[1] == X:
                    break

        Y = str(temp_list[2])

        # Appending Unstack operation
        planning_stack.append("unstack " + str(X) + " " + str(Y))
        planning_stack.append("arm_empty")
        planning_stack.append("on " + str(X) + " " + str(Y))
        planning_stack.append("clear " + str(X))

"""To satisfy arm_empty predicate we find the block that is currently held by searching for the holding predicate in the current_state list and executing the putdown operation for the same block"""
def arm_empty():

    check = "holding "

    for predicate in current_state:
        if check in predicate:
            tmp_list = predicate.split()
            Y = str(tmp_list[1])

            planning_stack.append("putdown " + str(Y))
            planning_stack.append("holding " + str(Y))


# from functions import *

if __name__ == "__main__":

    prCyan("==================== GOAL STATE PLANNER ====================")

    print("|-----------------------------------------------------------|")
    #steps_for_goal is the final output list that will hold onto the actions required to reach the goal state
    steps_for_goal = []

    #intial state is taken and split into suitable elements using | delimiter
    input_string = input(Fore.BLUE + "Please enter the start state :- \n")
    print(Style.RESET_ALL)
    current_state = input_string.split("|")

    #goal statie is taken and split into suitable elements using | delimiter
    goal_state = []
    input_string = input(Fore.BLUE + "Please enter the goal state :- \n")
    print(Style.RESET_ALL)
    goal_state = input_string.split("|")

    #input states are output on terminal for recheck
    prYellow("\nEntered Start State:- " + convert_list(current_state))
    prYellow("\nEntered Goal State:- " + convert_list(goal_state) + "\n")

    # actions and predicates
    actions = ["stack", "unstack", "pickup", "putdown"]
    predicates = ["on", "clear", "arm_empty", "holding", "on_table"]

    prRed("\nPlanning Starts----------------------------------------------------------------\n")

    # MAIN ALGORITHM IMPLIMENTATION

    for predicate in goal_state:
        planning_stack.append(predicate)

    while len(planning_stack) > 0:
        print("Planning Stack:- \n")
        prLightPurple(convert_list(planning_stack) + "\n")
        print("Current World State :- \n")
        prLightPurple(convert_list(current_state) + "\n")
        top = planning_stack.pop()
        sub_goal_list = top.split()

        if sub_goal_list[0] in predicates:  # if top of stack is predicate

            if top in current_state:  # if predicate is true:
                continue  # You have already popped the predicate from stack

            # push corresponding action that will satisfy that predicate onto stack and push preconditions of that action
            if sub_goal_list[0] == "on":
                on(sub_goal_list[1], sub_goal_list[2])
            elif sub_goal_list[0] == "on_table":
                on_table(sub_goal_list[1])
            elif sub_goal_list[0] == "clear":
                clear(sub_goal_list[1])
            elif sub_goal_list[0] == "holding":
                holding(sub_goal_list[1])
            elif sub_goal_list[0] == "arm_empty":
                arm_empty()

        if sub_goal_list[0] in actions:  # if top of stack is action
            # Already popped above

            # perform the action i.e add and delete it's effects from current state
            if sub_goal_list[0] == "stack":
                stack(sub_goal_list[1], sub_goal_list[2])
            elif sub_goal_list[0] == "unstack":
                unstack(sub_goal_list[1], sub_goal_list[2])
            elif sub_goal_list[0] == "pickup":
                pickup(sub_goal_list[1])
            elif sub_goal_list[0] == "putdown":
                putdown(sub_goal_list[1])

            # add that action to the actual plan
            steps_for_goal.append(top)

    prRed("\nPlanning Ends------------------------------------------------------------------\n")

    prPurple("Final state reached:- " + convert_list(current_state))

    prGreen("\nPlan generated to reach goal state:- \n")

    for step in steps_for_goal:
        split = step.split()
        if len(split) == 3:
            prGreen(split[0] + ": " + split[1]+" and "+split[2])
        elif len(split) == 2:
            prGreen(split[0] + ": " + split[1])
        elif len(split) == 1:
            prGreen(split[0])
            
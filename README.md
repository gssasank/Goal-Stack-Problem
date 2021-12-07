# Assignment - 4

## Introduction to Planning Systems

A key ability of intelligent systems is planning. Planning refers to the process of computing several steps of the problem before executing them. Planning is an advanced problem-solving paradigm that increases the autonomy and flexibility of systems by constructing sequences of actions that help them in achieving their goals. Planning is particularly effective because it controlling combinatorial explosions while solving problems. 

## Components of Planning Systems

- **Representation of States:** For representation of states, planners decompose the world into logical conditions and then represent a state as a conjunction of predicate atoms (positive literals).

- **Representation of Goals:** A goal is a partially specified state and is represented as a conjunction of predicate atoms (ground literals).

- **Representation of Actions:** An action is specified in terms of preconditions (that must hold true before the action can be executed) and effects (that occur when the action is executed).

    The goal stack method is one of the earliest methods that were used for solving compound goals, which may not interact with each other. This approach was used by STRIPS systems. In this system, the problem solver makes use of a single stack containing goals as well as operators that have been proposed to satisfy these goals. In goal stack method, individual sub goals are solved linearly and then, at the final stage, the conjoined sub goals are solved. Plans generated by this method contain complete sequence of operations for solving the first goal followed by complete sequence of operations for the next one, and so on. 

## Block World Problem

The block world problem consists of handling blocks and generating a new pattern from a given pattern. Our aim is to enumerate a list of strategies that will lead to a list of steps, which might help a computer solve such problems. These few assumptions we make while solving the block world problem:

``` 
- All blocks are of same size and shape.
- Blocks can be stacked on each other.
- There is a flat surface on which these blocks are placed on.
- There is a robot arm that can manipulate the blocks, it can only hold and move one block at a time.
```

In the block world problem, a state is described by a set of predicates, which represent the facts that are true in that state. For every action, we describe the changes that the action makes to the state description. In addition, some statements regarding the things which remain unchanged by applying actions are also to be specified. 

## Predicates and Operators

<img src="C:\Users\Sasank\AppData\Roaming\Typora\typora-user-images\image-20211111145113549.png" alt="image-20211111145113549" style="zoom: 67%;" />

<img src="C:\Users\Sasank\AppData\Roaming\Typora\typora-user-images\image-20211111145134055.png" alt="image-20211111145134055" style="zoom:67%;" />

## Pseudocode

The pseudocode for the main algorithm is as follows:

```
{
  -> Push conjoined sub goals and individual sub goals onto Stack;
  -> flag = true;
    while(Stack != {} and flag = true) do
        { If top element of stack is an operator then
            {
           -> POP it and add to PLAN_QUEUE of operations to be performed in a plan;
           -> Generate new state from current state by using ADD and DEL lists of an operator
            }
          Else
            { If top of the stack is sub goal and is true in the current state then POP it
              Else
              { 
              -> Identify operators that satisfy top goal of the stack;
              -> If (no operator exists) then set flag = false
                Else
                {
              -> Choose one operator that satisfies the sub goal (use some heuristic);
              -> POP sub goal and PUSH chosen operator along with its preconditions in the stack;
                }
              }
            }
        -> If (flag = false) then problem solver returns no plan else returns the plan stored in
           PLAN_QUEUE for the problem;
        }
}            
```

## Algorithms Used

### Actions

- **stack(X, Y):** 
    *adds:* on X Y,clear X and arm_empty predicates to the planning_stack list
    *removes:* holding X and clear Y predicates from the current_state list

``` Python
def stack(X, Y):
    current_state.append("on " + str(X) + " " + str(Y))
    current_state.append("clear " + str(X))
    current_state.append("arm_empty")
    current_state.remove("holding " + str(X))
    current_state.remove("clear " + str(Y))
```

- **unstack(X, Y):** 
    *adds:* holding X,clear Y predicates to the planning_stack list
    *removes:* on X,Y,clear X and arm_empty predicates from the current_state list

```Python
def unstack(X, Y):
    current_state.append("holding " + str(X))
    current_state.append("clear " + str(Y))
    current_state.remove("on " + str(X) + " " + str(Y))
    current_state.remove("clear " + str(X))
    current_state.remove("arm_empty")
```

- **pickup(X):** 
    *adds:* holding X predicate to the planning_stack list
    *removes:* arm_empty, on_table X and clear X predicates from the current_state list

``` Python
def pickup(X):
    current_state.append("holding " + str(X))
    current_state.remove("arm_empty")
    current_state.remove("on_table " + str(X))
    current_state.remove("clear " + str(X))
```

- **putdown(X):** 
    *adds:* arm_empty, on_table X and clear X predicates to the planning_stack list
    *removes:* holding X predicate from the current_state list

```Python
def putdown(X):
    current_state.append("arm_empty")
    current_state.append("on_table " + str(X))
    current_state.append("clear " + str(X))
    current_state.remove("holding " + str(X))
    
```

### Predicates

- **on(X, Y):** 
    To statisfy on(X,Y) predicate we need to execute a stack(X,Y) operation which has two preconditions i.e. holding(X) and clear(Y). These are all added to the planning_stack list.

``` Python
def on(X, Y):
    planning_stack.append("stack " + str(X) + " " + str(Y))
    planning_stack.append("holding " + str(X))
    planning_stack.append("clear " + str(Y))
```

- **on_table(X):** 
    To statisfy on_table(X) predicate we need to execute a putdown(X) operation which has on3 precondition i.e., holding(X). These are all added to the planning_stack list.

``` Python
def on_table(X):
    planning_stack.append("putdown " + str(X))
    planning_stack.append("holding " + str(X))
```

- **clear(X):** 

    To satisfy clear(X) predicate we need to execute an unstack(Y,X) operation which has three preconditions i.e., arm_empty,on(Y,X) and clear(Y). These are all added to the planning_stack list. We have also taken care of the case where the program could not resolve solving the clear predicate when the block was already being held.

```python
def clear(X):

    check ="holding " + str(X)
    
    if check in current_state:
        planning_stack.append("putdown " + str(X))
    else:
        check = "on "
        for predicate in current_state:
            if check in predicate:
                temp_list = predicate.split()
                if temp_list[2] == X:
                    break

        Y = str(temp_list[1])

        planning_stack.append("unstack " + str(Y) + " " + str(X))
        planning_stack.append("arm_empty")
        planning_stack.append("on " + str(Y) + " " + str(X))
        planning_stack.append("clear " + str(Y))
```

- **holding(X):** 
    To statisfy holding(X) predicate we need to check whether the block X is on table or if it is on top of another block.   If the block is on table we execute the pickup(X) operation and its three preconditions i.e. arm_empty,on_table (X) and clear (X) are all added to the planning_stack list.
    If block X is not on the table then we execute unstack(X,Y) operation and its three preconditions i.e. arm_empty,on (X,Y) and clear (X) are all added to the planning_stack list.

```python
def holding(X)
    check = "on_table " + str(X)

    if check in current_state:
        planning_stack.append("pickup " + str(X))
        planning_stack.append("arm_empty")
        planning_stack.append("on_table " + str(X))
        planning_stack.append("clear " + str(X))

    else:

        check = "on "

        for predicate in current_state:
            if check in predicate:
                temp_list = predicate.split()

                if temp_list[1] == X:
                    break

        Y = str(temp_list[2])

        planning_stack.append("unstack " + str(X) + " " + str(Y))
        planning_stack.append("arm_empty")
        planning_stack.append("on " + str(X) + " " + str(Y))
        planning_stack.append("clear " + str(X))
```

- **arm_empty():** 
    To satisfy arm_empty predicate we find the block that is currently held by searching for the holding predicate in the current_state list and executing the putdown operation for the same block.

```python
def arm_empty():

    check = "holding "

    for predicate in current_state:
        if check in predicate:
            tmp_list = predicate.split()
            Y = str(tmp_list[1])

            planning_stack.append("putdown " + str(Y))
            planning_stack.append("holding " + str(Y))
```

### Goal Stack Algorithm

The algorithm taught in class was slightly modified to print the current state and the planning stack while the loop is running. Due to the in-built features of Python language, we were also able to eliminate the need for a flag.

We push the subgoals onto the stack after we clean the user-inserted data and extract the parts necessary to us (we do this by removing our delimiter "|" and then splitting the input into a list). Based on the actions and predicates present in sub_goal_list, we perform the specific actions by calling their respective functions. After all the steps, we add the action to the final list of steps needed to reach the goal (steps_for_goal) .

``` python
while len(planning_stack) > 0:
        print("Planning Stack:- \n")
        prLightPurple(convert_list(planning_stack) + "\n")
        print("Current World State :- \n")
        prLightPurple(convert_list(current_state) + "\n")
        top = planning_stack.pop()
        sub_goal_list = top.split()

        if sub_goal_list[0] in predicates:  

            if top in current_state:  
                continue  
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

        if sub_goal_list[0] in actions: 

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
```





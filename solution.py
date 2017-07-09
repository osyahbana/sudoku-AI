assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

#I'm defining a bunch of variables that I'm going to use later on. Most were taken from the quizzes
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diag_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    #creating an empty list of values for us to append later]
    values = []
    all_digits = '123456789'
    #iterating for every element in the grid, if it's empty, append with alldigits
    for i in grid:
        if i == '.':
            values.append(all_digits)
        #if it's not empty, append the values with the value of i
        elif i in all_digits:
            values.append(i)
    assert len(values) == 81
    #with the zip function we are making a list with tuple between name of boxes and the value from values
    #dict function is turning that zip into a nice dictionary structure
    return dict(zip(boxes, values))
    


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    #I gotta be honest, I'm just copying this from utils from quizzes
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """This code goes through each of the box within the unit and list the box that contains a digit,
    say 1. If it finds exactly one box that contains the digit (in this case 1), then it assign value 1
    to that box, and eliminate from its other peers."""
    #we eliminate the probable digit from all the peers if one of the box already have that number
    #we find all the box that is already solved and bind it to solved_values
    #iterate through the element in values.keys and put the element to list if the length is 1
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    #iterate every element in solved_values
    for box in solved_values:
        #digit is the value of solved_values
        digit = values[box]
        #for every peers in the box that is already solved
        for peer in peers[box]:
            #we replace the solved digit with '', effectively deleting them from the peers
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """This function takes in input in dictionary form. It goes through all units, and if there's 
    a unit with digit that only fits one possible box, it will assign that digit to that box, and delete from
    everywhere else"""
    #iterate on every unit list
    for unit in unitlist:
        #for every digit
        for digit in '123456789':
            #give value to dplaces only if the iterated digit is the value of the box
            dplaces = [box for box in unit if digit in values[box]]
            #if the value of dplaces is already only 1, return that digit
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """    
    #put a value to list named twins that iterate values.keys() if only the length of value is 2
    twins = [box for box in values.keys() if len(values[box]) == 2]
    #iterate for every element in that previous list, to check what digit is in twins
    for box in twins:
        digit = values[box]
        #iterate for every element to find peers
        for peer in peers[box]:
            # checking for the value in the peers whether they have twins
            if digit==values[peer]:
                for i in units[box]:
                    #if there's twin in both the box and the peers
                    if box in i and peer in i:
                        for s in i:
                            #eliminating the twins value from peers of the same box
                            if s not in [box,peer]:
                                for d in digit:
                                    values[s] = values[s].replace(d,'')

    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        #checking how many box already have values. We will use this on iteration to check whether we are solving anything
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        #use eliminate strategy
        values = eliminate(values)
        #use only choice strategy
        values = only_choice(values)
        #use naked twins strategy
        values = naked_twins(values)
        #check how many box are we solving
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        #change stalled to True to stop the while statement
        stalled = solved_values_before == solved_values_after
        #sanity check
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid if type(grid) == dict else grid_values(grid)
    return search(values)

def search(values):
    #call the reduce function
    values = reduce_puzzle(values)
    if values is False:
        return False #to prevent the function from infinite loop if it already failed up front
    if all(len(values[s]) == 1 for s in boxes):
        return values #saving computing power and return solved
    #Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
     # Now use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = solve(new_sudoku)
        if attempt:
            return attempt

if __name__ == '__main__':
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

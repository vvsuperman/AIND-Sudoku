digits = '123456789'
rows = 'ABCDEFGHI'
cols = '123456789'


assignments = []


def cross(A, B):
    #"Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows,cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units=[['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers    

    for unit in unitlist:
        twins_value = []
        for key1 in unit:
            for key2 in unit:
                if values[key1]==values[key2] and len(values[key1])==2 and key1!=key2:
                    twins_value.append(key1)

        if len(twins_value)==2:
                #print(twins_value,values[twins_value[0]],values[twins_value[1]])
                for value in values[twins_value[0]]:  
                    #print(value)              
                    for key in unit:
                        #print(key,values[key])
                        if key!=twins_value[0] and key != twins_value[1] and len(values[key])>1:
                            #print('deal value..........',values[key],value)
                            values[key] = values[key].replace(value,'')
    print('after value......')
    display(values)
    return values




def grid_values(grid):
   
    values=[]
    for c in grid:
        if c=='.':
            values.append(digits)
        elif c in digits:
            values.append(c)        
    assert(len(values)==81)
    return dict(zip(boxes,values))



def display(values):
    
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            if values[peer] != digit:
                values[peer] = values[peer].replace(digit,'')
                
    return values


def only_choice(values):
    new_values = values.copy()  # note: do not modify original values

    for unit in unitlist:
        for c in digits:
           unit_box = [box for box in unit if values[box] ==c]
           if len(unit_box)==1:
               new_values[unit_box[0]] = c
    return new_values 

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box])==1]
    stalled=False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box])==1])
        eliminate(values)
        only_choice(values)
        naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box])==1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    n,box = min((len(values[box]),box) for box in boxes if len(values[box])>1)
    for value in values[box]:
        new_values = values.copy()
        new_values[box] = value
        attemp = search(new_values)
        if attemp:
            return attemp



def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
        

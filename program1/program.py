from copy import deepcopy
from unipq import unipq
from functools import partial

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))

def swapper(input_state, dir):
    state = deepcopy(input_state)
    swap_idx = index_2d(state, 0)
    try:
        if (dir == 'up'):
            if (swap_idx[0]-1 < 0):
                raise IndexError('went negative!')
            state[swap_idx[0]-1][swap_idx[1]], state[swap_idx[0]][swap_idx[1]] = state[swap_idx[0]][swap_idx[1]], state[swap_idx[0]-1][swap_idx[1]]
        if (dir == 'down'):
            state[swap_idx[0]+1][swap_idx[1]], state[swap_idx[0]][swap_idx[1]] = state[swap_idx[0]][swap_idx[1]], state[swap_idx[0]+1][swap_idx[1]]
        if (dir == 'right'):
            state[swap_idx[0]][swap_idx[1]+1], state[swap_idx[0]][swap_idx[1]] = state[swap_idx[0]][swap_idx[1]], state[swap_idx[0]][swap_idx[1]+1]
        if (dir == 'left'):
            if (swap_idx[1]-1 < 0):
                raise IndexError('went negative!')
            state[swap_idx[0]][swap_idx[1]-1], state[swap_idx[0]][swap_idx[1]] = state[swap_idx[0]][swap_idx[1]], state[swap_idx[0]][swap_idx[1]-1]
    except IndexError:
        return
    return state

def move(state):
	return [(s, a, 1) for s, a in [(swapper(state, dir), dir) for dir in ['up', 'down', 'right', 'left']] if s != None]

def node_constructor(saw, heuristic, prev_states, prev_cost):
    new_history = deepcopy(prev_states)
    new_history.append(saw[0])
    return {'cost': saw[2] + prev_cost + heuristic(saw[0]),
            'prev': new_history,
            'action': saw[1],
            'state': saw[0]}

def null_heur(start, goal):
    return 0

def mandistheur(start, goal):
    tot_sum = 0
    for col, i in enumerate(start):
        for row, j in enumerate(i):
            if j != 0:
                cur_goal = index_2d(goal, j)
                tot_sum += abs(col - cur_goal[0]) + abs(row - cur_goal[1])
    return tot_sum 
    
def astar(start, goal_func, heuristic):
    examined_list = set()
    unexamined = unipq()
    cur_node = node_constructor((start, None, heuristic(start)), heuristic, list(), 0)
    unexamined.add((cur_node["cost"], cur_node))
    while(not unexamined.empty()):
        current = unexamined.pop()
        if str(current[1]["state"]) in examined_list:
            continue
        examined_list.add(str(current[1]["state"]))
        if goal_func(current[1]['state']):
            return current[1]['prev']
        for i in move(current[1]['state']):
            cur_node = node_constructor(i, heuristic, current[1]['prev'], current[1]['cost'])
            if (str(cur_node["state"]) not in examined_list):
                unexamined.add((cur_node["cost"], cur_node))
    return []

def tile_solver(start, goal_inp):
    def goal(state):
        return state == goal_inp
    heuristic = partial(mandistheur, goal = goal_inp)
    empty_loop = True
    for index, i in enumerate(astar(start, goal, heuristic)):
        empty_loop = False
        print index, ": ", i
    else:
        if empty_loop:
            print "No solution found for " + str(start) + " to " + str(goal_inp)
        else:
            empty_loop = True
        
    print

goal_state = [[1,2,3], [4,5,6],[7,8,0]]
start_states = [ [[6, 4, 2],[1, 5, 3],[7, 0, 8]],
                 [[6, 4, 2],[8, 5, 3],[1, 0, 7]],
                 [[8, 0, 7],[6, 5, 4],[3, 2, 1]],
                 [[6, 4, 7],[8, 5, 0],[3, 2, 1]],
                 [[1, 2, 3],[4, 5, 6],[8, 7, 0]] ]

map((lambda x : tile_solver(x, goal_state)), start_states)

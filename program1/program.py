#! /bin/python2

# Joshua Marple, Feb 2015
# 

# from unipq import unipq
from Queue import PriorityQueue
from functools import partial
import timeit
import time
import copy

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))

def swapper(input_state, dir):
    state = []
    for i in input_state:
        state.append(list(i))
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

def node_constructor(saw, heuristic, prev):
    heuristic_cost = heuristic(saw[0])
    if prev != None:
        prev_cost = prev['g']
    else:
        prev_cost = 0
    return {'cost': saw[2] + prev_cost + heuristic_cost,
            'g': saw[2] + prev_cost,
            'h': heuristic_cost,
            'f': saw[2] + prev_cost + heuristic_cost,
            'prev': prev,
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

def dfs(start, goal_func, depth, cur_depth, examined_list, inp_history):
    # history = copy.deepcopy(inp_history)
    history = [x for x in inp_history]
    examined_list[str(start)] = True
    history.append(str(start))
    if (cur_depth != depth):
        for i in move(start):
            try:
                # print(examined_list[str(i)])
                if (examined_list[str(i)] == True):
                    break
            except KeyError:
                pass
            # print(i)
            if goal_func(i[0]):
                print("found it!")
                history.append(i[0])
                return history
                
            tmp_solution = dfs(i[0], goal_func, depth, cur_depth+1, examined_list, history)
            if tmp_solution != None:
                # tmp_solution.append(i[0])
                return tmp_solution
            
    return None

def ids(start, goal_func, heuristic):
    depth = 20
    while(depth < 32):
        print(depth)
        solution = dfs(start, goal_func, depth, 0, {}, [])
        if solution != None:
            return solution
        depth += 1
    return 0
        
    
def astar(start, goal_func, heuristic):
    examined_list = {}
    unexamined = PriorityQueue()
    cur_node = node_constructor((start, None, 0), heuristic, None)
    unexamined.put((cur_node["cost"], cur_node))
    while(not unexamined.empty()):
        current = unexamined.get()
        try:
            if (examined_list[str(current[1]["state"])] == True):
                continue
        except KeyError:
            examined_list[str(current[1]["state"])] = True
        if goal_func(current[1]['state']):
            return_list = []
            tmp = current[1]
            while (tmp != None):
                return_list.append((tmp['action'], tmp['state'], tmp['g'], tmp['h'], tmp['f']))
                tmp = tmp['prev']
            return [x for x in reversed(return_list)]
        for i in move(current[1]['state']):
            cur_node = node_constructor(i, heuristic, current[1])
            try:
                examined_list[str(cur_node["state"])] == True
            except KeyError:
                unexamined.put((cur_node["cost"], cur_node))
    return len(examined_list)

def tile_solver(start, goal_inp, inp_heuristic):
    def goal(state):
        return state == goal_inp
    heuristic = partial(inp_heuristic, goal = goal_inp)
    solution = ids(start, goal, heuristic)
    if isinstance(solution, (int, long)):
        print "No solution found, examined ", solution, " nodes."
    else:
        for index, i in enumerate(solution):
            print index, ": ", i
        
    print

goal_state = [[1,2,3], [4,5,6],[7,8,0]]
start_states = [ [[6, 4, 2],[1, 5, 3],[7, 0, 8]],
                 [[6, 4, 2],[8, 5, 3],[1, 0, 7]],
                 [[8, 0, 7],[6, 5, 4],[3, 2, 1]],
                 [[6, 4, 7],[8, 5, 0],[3, 2, 1]],
                 [[1, 2, 3],[4, 5, 6],[8, 7, 0]] ]

print("testing manhattan distance heuristic")
# print(timeit.timeit('map((lambda x : tile_solver(x, goal_state, mandistheur)), start_states)', number= 1, setup = "from __main__ import tile_solver, goal_state, start_states, null_heur, mandistheur"))

tile_solver(  [[6, 4, 2],[8, 5, 3],[1, 0, 7]], goal_state, mandistheur)

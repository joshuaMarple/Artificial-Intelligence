from copy import deepcopy
from unipq import unipq

def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))

def swapper(input_state, dir):
	state = deepcopy(input_state)
	swap_idx = index_2d(state, 0)
	if (dir == 'up'):
		try:
                    if (swap_idx[0]-1 < 0):
                        raise IndexError('went negative!')
                    state[swap_idx[0]-1][swap_idx[1]], state[swap_idx[0]][swap_idx[1]] = state[swap_idx[0]][swap_idx[1]], state[swap_idx[0]-1][swap_idx[1]]
		except IndexError:
			return
	if (dir == 'down'):
		try:
                    state[swap_idx[0]+1][swap_idx[1]], state[swap_idx[0]][swap_idx[1]] = state[swap_idx[0]][swap_idx[1]], state[swap_idx[0]+1][swap_idx[1]]
		except IndexError:
			return
	if (dir == 'right'):
		try: 
			state[swap_idx[0]][swap_idx[1]+1], state[swap_idx[0]][swap_idx[1]] = state[swap_idx[0]][swap_idx[1]], state[swap_idx[0]][swap_idx[1]+1]
		except IndexError:
			return
	if (dir == 'left'):
		try:
                    if (swap_idx[1]-1 < 0):
                        raise IndexError('went negative!')
                    state[swap_idx[0]][swap_idx[1]-1], state[swap_idx[0]][swap_idx[1]] = state[swap_idx[0]][swap_idx[1]], state[swap_idx[0]][swap_idx[1]-1]
		except IndexError:
			return
	return state


def move(state):
	return [(s, a, 1) for s, a in [(swapper(state, dir), dir) for dir in ['up', 'down', 'right', 'left']] if s != None]

    
def node_constructor(saw, prev, goal):
    new_history = deepcopy(prev)
    new_history.append(saw[0])
    return {'cost': saw[2] + mandistheur(saw[0], goal),
		 'prev': new_history,
            # 'prev' : None,
		 'action': saw[1],
		 'state': saw[0]
		}



def mandistheur(start, goal):
	tot_sum = 0
	for col, i in enumerate(start):
		for row, j in enumerate(i):
			cur_goal = index_2d(goal, j)
			tot_sum += abs(col - cur_goal[0]) + abs(row - cur_goal[1])
	return tot_sum 


def key_gen(item):
    tmp_dict = deepcopy(item[1])
    tmp_dict.pop("prev", None)
    return str((item[0], tmp_dict))
    
def astar(start, goal):
    examined_list = set()
    unexamined = unipq()
    cur_node = node_constructor((start, None, mandistheur(start, goal)), list(), goal)
    unexamined.add((cur_node["cost"], cur_node))
    while(not unexamined.empty()):
        current = unexamined.pop()
        if str(current[1]["state"]) in examined_list:
            continue
        examined_list.add(str(current[1]["state"]))
        if current[1]['state'] == goal:
            return current[1]['prev']
        for i in move(current[1]['state']):
            cur_node = node_constructor(i, current[1]['prev'], goal)
            if (str(cur_node["state"]) not in examined_list):
                unexamined.add((cur_node["cost"], cur_node))
        






# print(astar([[1,2,3],[4,5,6],[7,0,8]], [[1,2,3], [4,5,6],[0,7,8]]))
print(astar([[7,2,4],[5,0,6],[8,3,1]], [[0,1,2], [3,4,5],[6,7,8]]))
# print(mandistheur([[1,2,3], [4,5,6], [7,9,8]], [[1,2,3], [4,5,6], [7,8,9]]))
# print(index_2d([[1,2,3], [4,5,6], [7,8,9]], 3))
# print(move([[1,2,3], [4,5,6], [7,0,8]]))














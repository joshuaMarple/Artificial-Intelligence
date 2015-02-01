
# goals = [[[1,2,3],[4,5,6],[7,8,0]]]
from copy import deepcopy
# from Queue import PriorityQueue
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
			state[swap_idx[0]][swap_idx[1]-1], state[swap_idx[0]][swap_idx[1]] = state[swap_idx[0]][swap_idx[1]], state[swap_idx[0]][swap_idx[1]-1]
		except IndexError:
			return
	return state


def move(state):
	return [(s, a, 1) for s, a in [(swapper(state, dir), dir) for dir in ['up', 'down', 'right', 'left']] if s != None]

    
def node_constructor(saw, prev, goal):
	return {'cost': saw[2] + mandistheur(saw[0], goal),
		 'prev': None,
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

    
def astar(start, goal):
    # examined = PriorityQueue()
    examined_list = set()
    unexamined = unipq()
    # unexamined_list = set()
	# print(move(start))
    # print(start)
    # for i in move(start):
    cur_node = node_constructor((start, None, mandistheur(start, goal)), None, goal)
    unexamined.add((cur_node["cost"], cur_node))
    while(not unexamined.empty()):
        current = unexamined.pop()
        if str(current) in examined_list:
            continue
        examined_list.add(str(current))
        print("goal checking")
        print(current[1]['state'], current[1]['cost'])
        if current[1]['state'] == goal:
            print("success!")
            return
        
        print("move/add unexamined")
        for i in move(current[1]['state']):
            cur_node = node_constructor(i, current, goal)
            if (str((cur_node["cost"], cur_node)) not in examined_list):
                unexamined.add((cur_node["cost"], cur_node))
        







astar([[1,2,3],[4,5,6],[7,0,8]], [[1,3,2], [5,4,6],[0,7,8]])
# print(mandistheur([[1,2,3], [4,5,6], [7,9,8]], [[1,2,3], [4,5,6], [7,8,9]]))
# print(index_2d([[1,2,3], [4,5,6], [7,8,9]], 3))
# print(move([[1,2,3], [4,5,6], [7,0,8]]))














import sys
import puzz
import pdqpq


MAX_SEARCH_ITERS = 100000
GOAL_STATE = puzz.EightPuzzleBoard("012345678")


def solve_puzzle(start_state, strategy):
    """Perform a search to find a solution to a puzzle.
    
    Args:
        start_state: an EightPuzzleBoard object indicating the start state for the search
        flavor: a string indicating which type of search to run.  Can be one of the following:
            'bfs' - breadth-first search
            'ucost' - uniform-cost search
            'greedy-h1' - Greedy best-first search using a misplaced tile count heuristic
            'greedy-h2' - Greedy best-first search using a Manhattan distance heuristic
            'greedy-h3' - Greedy best-first search using a weighted Manhattan distance heuristic
            'astar-h1' - A* search using a misplaced tile count heuristic
            'astar-h2' - A* search using a Manhattan distance heuristic
            'astar-h3' - A* search using a weighted Manhattan distance heuristic
    
    Returns: 
        A dictionary containing describing the search performed, containing the following entries:
            'path' - a list of 2-tuples representing the path from the start state to the goal state 
                (both should be included), with each entry being a (str, EightPuzzleBoard) pair 
                indicating the move and resulting state for each action.  Omitted if the search 
                fails.
            'path_cost' - the total cost of the path, taking into account the costs associated 
                with each state transition.  Omitted if the search fails.
            'frontier_count' - the number of unique states added to the search frontier at any
                point during the search.
            'expanded_count' - the number of unique states removed from the frontier and expanded 
                (i.e. have successors generated).
    """
    strategy = strategy.split("-")
    if(strategy[0]=="bfs"):
        return bfs(start_state)
    
    if(strategy[0]=="ucost"):
         return ucost(start_state)

    if(strategy[0]=="greedy"):
        if(strategy[1]=="h1"):
            return greedy(start_state,numberofMisplacedtiles)
        if(strategy[1]=="h2"):
            return greedy(start_state,manhattendistance)
        if(strategy[1]=="h3"):
            return greedy(start_state,modifiedmanhattan)

    if(strategy[0]=="astar"):
        if(strategy[1]=="h1"):
            return astar(start_state,numberofMisplacedtiles)
        if(strategy[1]=="h2"):
            return astar(start_state,manhattendistance)
        if(strategy[1]=="h3"):
            return astar(start_state,modifiedmanhattan)
   
    
   
    

    results = {
        'frontier_count': 0,
        'expanded_count': 0,
    }
    # 
    # fill in the function body here
    #

    return results

def bfs(start_state):
    thisdictpath = {}
    thisdictcost = {}
    thisdictpath[start_state.__str__()] = copy([],("start", start_state.__str__()))
    thisdictcost[start_state.__str__()] = 0
    frontierCount = 0
    frontier =  pdqpq.PriorityQueue()
    explored = set()
    frontier.add(start_state) 
    frontierCount = 1 
    while frontier.empty()!=True:
        node = frontier.pop()
        explored.add(node)
        succs = node.successors()

        if node.__str__()==GOAL_STATE.__str__(): 
            results = {
                'path': thisdictpath[node.__str__()],
                'path_cost': thisdictcost[node.__str__()],
                'frontier_count': frontierCount,
                'expanded_count': len(explored),
                }
            return results
       

        for n in succs:
            state = succs[n]
            print(state)
            print(succs)
            return

            if (state not in frontier) and (state not in explored):
                thislist = copy(thisdictpath[node.__str__()],(n,state.__str__()))
                thisdictpath[state.__str__()] = thislist
                thisdictcost[state.__str__()] = thisdictcost[node.__str__()]+findCost(node.__str__(),state.__str__())
    
                if state.__str__()==GOAL_STATE.__str__(): 
                    results = {
                        'path': thisdictpath[state.__str__()],
                        'path_cost': thisdictcost[state.__str__()],
                        'frontier_count': frontierCount,
                        'expanded_count': len(explored),
                        }
                    return results
                else:
                    frontier.add(state)
                    frontierCount+=1


    results = {
        'frontier_count': frontierCount,
        'expanded_count': len(explored),
    }
    return results

    
def ucost(start_state):
    thisdictpath = {}
    thisdictcost = {}
    thisdictpath[start_state.__str__()] = copy([],("start", start_state.__str__()))
    thisdictcost[start_state.__str__()] = 0
   
    frontierCount = 0
    frontier =  pdqpq.PriorityQueue()
    explored = set()
    frontier.add(start_state,0) 
    frontierCount = 1 
    while frontier.empty()!=True:
        node = frontier.pop()
        if node.__str__()==GOAL_STATE.__str__(): 
                    results = {
                        'path': thisdictpath[node.__str__()],
                        'path_cost': thisdictcost[node.__str__()],
                        'frontier_count': frontierCount,
                        'expanded_count': len(explored),
                        }
                    return results
        explored.add(node)
        succs = node.successors()
        

        for n in succs:
            state = succs[n]
            cost = thisdictcost[node.__str__()]+findCost(node.__str__(),state.__str__())
            thislist = copy(thisdictpath[node.__str__()],(n,state.__str__()))
            if (state not in frontier) and (state not in explored):
                thisdictpath[state.__str__()] = thislist
                thisdictcost[state.__str__()] = cost
                frontierCount+=1
                frontier.add(state,cost)
            elif (state in frontier) and(thisdictcost[state.__str__()] > cost):
                thisdictpath[state.__str__()] = thislist
                thisdictcost[state.__str__()] = cost
                frontier.add(state, cost)

    results = {
        'frontier_count': frontierCount,
        'expanded_count': len(explored),
    }
    return results

def greedy(start_state,thefunction):
    thisdictpath = {}
    thisdictcost = {}
    thisdictpath[start_state.__str__()] = copy([],("start", start_state.__str__()))
    thisdictcost[start_state.__str__()] = 0
   
    frontierCount = 0
    frontier =  pdqpq.PriorityQueue()
    explored = set()
    frontier.add(start_state,thefunction(start_state.__str__())) 
    frontierCount = 1 
    while frontier.empty()!=True:
        node = frontier.pop()
        if node.__str__()==GOAL_STATE.__str__(): 
                    results = {
                        'path': thisdictpath[node.__str__()],
                        'path_cost': thisdictcost[node.__str__()],
                        'frontier_count': frontierCount,
                        'expanded_count': len(explored),
                        }
                    return results
        explored.add(node)
        succs = node.successors()
        

        for n in succs:
            state = succs[n]
            cost = thisdictcost[node.__str__()]+findCost(node.__str__(),state.__str__())
            thislist = copy(thisdictpath[node.__str__()],(n,state.__str__()))
            priority = thefunction(state.__str__())
            if (state not in frontier) and (state not in explored):
                thisdictpath[state.__str__()] = thislist
                thisdictcost[state.__str__()] = cost
                frontier.add(state, priority)
                frontierCount+=1
            elif (state in frontier) and(thisdictcost[state.__str__()] > cost):
                thisdictpath[state.__str__()] = thislist
                thisdictcost[state.__str__()] = cost


    results = {
        'frontier_count': frontierCount,
        'expanded_count': len(explored),
    }
    return results
    
def astar(start_state,thefunction):
    thisdictpath = {}
    thisdictcost = {}
    thisdictpath[start_state.__str__()] = copy([],("start", start_state.__str__()))
    thisdictcost[start_state.__str__()] = 0
   
    frontierCount = 0
    frontier =  pdqpq.PriorityQueue()
    explored = set()
    frontier.add(start_state,thefunction(start_state.__str__())+0) 
    frontierCount = 1 
    while frontier.empty()!=True:
        node = frontier.pop()
        
        if node.__str__()==GOAL_STATE.__str__(): 
            results = {
                'path': thisdictpath[node.__str__()],
                'path_cost': thisdictcost[node.__str__()],
                'frontier_count': frontierCount,
                'expanded_count': len(explored),
                }
            return results
        explored.add(node)
        succs = node.successors()
        

        for n in succs:
            state = succs[n]
            cost = thisdictcost[node.__str__()]+findCost(node.__str__(),state.__str__())
            thislist = copy(thisdictpath[node.__str__()],(n,state.__str__()))
            priority = thefunction(state.__str__())
            if (state not in frontier) and (state not in explored):
                thisdictpath[state.__str__()] = thislist
                thisdictcost[state.__str__()] = cost
                frontierCount+=1
                frontier.add(state,cost+priority)
            elif (state in frontier) and(thisdictcost[state.__str__()] > cost):
                thisdictpath[state.__str__()] = thislist
                thisdictcost[state.__str__()] = cost
                frontier.add(state, cost+priority)

    results = {
        'frontier_count': frontierCount,
        'expanded_count': len(explored),
    }
    return results

   
def copy(list,tuple):
    newlist=[]
    for x in list:
        newlist.append(x)
    newlist.append(tuple)
    return newlist

def findCost(parent,child):
    index = parent.find('0')
    return (int(child[index])*int(child[index]))

def numberofMisplacedtiles(string):
    perfect="012345678"
    index=0
    count = 0
    for n in string:
        if n!=perfect[index]and n!='0':
            count+=1
        index+=1
    return  count

def manhattendistance(string):
    perfect="012345678"
    index=0
    count = 0
    for n in string:
        if n!=perfect[index] and n!='0':
            rowindex = (index)/3
            colIndex = (index)%3
            perfectIndex = perfect.index(n) 
            perfectrowindex = (perfectIndex)/3
            perfectcolIndex = (perfectIndex)%3
            count+= abs(perfectcolIndex-colIndex)+abs(perfectrowindex-rowindex)
        index+=1
    return  count

def modifiedmanhattan(string):
    perfect="012345678"
    index=0
    count = 0
    for n in string:
        if n!=perfect[index] and n!='0':
            rowindex = (index)/3
            colIndex = (index)%3
            perfectIndex = perfect.index(n) 
            perfectrowindex = (perfectIndex)/3
            perfectcolIndex = (perfectIndex)%3
            count+= (abs(perfectcolIndex-colIndex)+abs(perfectrowindex-rowindex))*int(n)*int(n)
        index+=1
    return  count








    


def print_summary(results):
    if 'path' in results:
        print("found solution of length {}, cost {}".format(len(results['path']), 
                                                            results['path_cost']))
        for move, state in results['path']:
            print("  {:5} {}".format(move, state))
    else:
        print("no solution found")
    print("{} states placed on frontier, {} states expanded".format(results['frontier_count'], 
                                                                    results['expanded_count']))


############################################

if __name__ == '__main__':

    start = puzz.EightPuzzleBoard(sys.argv[1])
    method = sys.argv[2]

    print("solving puzzle {} -> {}".format(start, GOAL_STATE))
    results = solve_puzzle(start, method)
    print_summary(results)

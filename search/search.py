# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class CustomNode:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def getName(self):
        return self.name

    def getCost(self):
        return self.cost

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def randomSearch(problem):

    import random

    current_state = problem.getStartState()
    solution = []

    while not problem.isGoalState(current_state):
        succesor = problem.getSuccessors(current_state)
        random_index = random.randint(0, len(succesor) - 1)
        next_state = succesor[random_index]
        action = next_state[1]
        current_state = next_state[0]
        solution.append(action)

    return solution


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """

    current_state = problem.getStartState()

    visited_nodes = []

    from util import Stack
    nodes = Stack()
    nodes.push((current_state, []))

    while not nodes.isEmpty():
        (current_node, actions) = nodes.pop()

        if current_node not in visited_nodes:
            visited_nodes.append(current_node)

            if problem.isGoalState(current_node):
                return actions

            for adjacent_node in problem.getSuccessors(current_node):
                (adj_node, action, cost) = adjacent_node
                nodes.push((adj_node, actions + [action]))
    
    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    current_state = problem.getStartState()

    visited_nodes = []

    from util import Queue
    nodes = Queue()
    nodes.push((current_state, []))

    while not nodes.isEmpty():
        (current_node, actions) = nodes.pop()

        if current_node not in visited_nodes:
            visited_nodes.append(current_node)
            if problem.isGoalState(current_node):
                return actions

            for adjacent_node in problem.getSuccessors(current_node):
                (adj_node, action, cost) = adjacent_node
                nodes.push((adj_node, actions + [action]))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    current_state = problem.getStartState()

    visited_nodes = set()

    from util import PriorityQueue
    nodes = PriorityQueue()
    nodes.push((current_state, [], 0), 0)

    while not nodes.isEmpty():
        (current_node, actions, cost) = nodes.pop()

        if current_node not in visited_nodes:
            visited_nodes.add(current_node)

            if problem.isGoalState(current_node):
                return actions

            for adjacent_node in problem.getSuccessors(current_node):
                (adj_node, action, total_cost) = adjacent_node
                new_cost = total_cost + cost
                nodes.push((adj_node, actions + [action], new_cost), new_cost)

    util.raiseNotDefined()

def nullHeuristic(state, problem = None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic = nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    current_state = problem.getStartState()

    visited_node = []
    from util import PriorityQueue
    from searchAgents import manhattanHeuristic
    #heuristic = manhattanHeuristic

    nodes = PriorityQueue()
    nodes.push((current_state, [], 0), 0)

    while not nodes.isEmpty():
        (current_node, actions, cost) = nodes.pop()

        if current_node not in visited_node:
            visited_node.append(current_node)

            if problem.isGoalState(current_node):
                return actions

            for adjacent_node in problem.getSuccessors(current_node):
                (adj_node, action, total_cost) = adjacent_node
                new_cost = total_cost + cost
                heur = new_cost + heuristic(adj_node, problem)
                nodes.push((adj_node, actions + [action], new_cost), heur)
            

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

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

import pprint

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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
"""
    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())

    "*** YOUR CODE HERE ***"
    closed = set()
    root_node = util.Node(problem.getStartState())
    fringe = util.Stack()
    fringe.push(root_node)


    while not fringe.isEmpty():
        node = fringe.pop()
        end_state = node.state
        # print ("node = ", node)
        # print ("end_state = ", end_state)

        if problem.isGoalState(end_state):
            # print("node.solution = ", node.solution)
            return node.solution()
        if end_state not in closed:
            closed.add(end_state)
            # print("closed = ", closed)
            for next_state, action, cost in problem.getSuccessors(end_state):
                child_node = util.Node(next_state, node, action)
                # print ("next_state = ", next_state, "action = ", action, "cost = ", cost)
                fringe.push(child_node)
    return None

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    closed = set()
    root_node = util.Node(problem.getStartState())
    fringe = util.Queue()
    fringe.push(root_node)

    while not fringe.isEmpty():
        node = fringe.pop()
        end_state = node.state
        # print ("node = ", node)
        # print ("end_state = ", end_state)

        if problem.isGoalState(end_state):
            # print("node.solution = ", node.solution)
            return node.solution()
        if end_state not in closed:
            closed.add(end_state)
            # print("closed = ", closed)
            for next_state, action, cost in problem.getSuccessors(end_state):
                child_node = util.Node(next_state, node, action)
                # print ("next_state = ", next_state, "action = ", action, "cost = ", cost)
                fringe.push(child_node)
    return None

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    closed = set()
    root_node = util.Node(problem.getStartState())
    #next_state, action, cost = problem.getSuccessors(root_node)
    #priority = 0
    fringe = util.PriorityQueue()
    fringe.push(root_node, 0)

    while not fringe.isEmpty():
        node = fringe.pop()
        end_state = node.state

        if problem.isGoalState(end_state):
            return node.solution()
        if end_state not in closed:
            closed.add(end_state)
            for next_state, action, cost in problem.getSuccessors(end_state):
                priority = node.path_cost + cost
                child_node = util.Node(next_state, node, action, priority)
                print("CHILD NODE", child_node)
                fringe.push(child_node, priority)
    return None



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch

x = dfs
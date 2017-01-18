# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import util
import sys
import random

from game import Agent


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 1)
    """

    def getAction(self, game_state):
        """
        Returns the best minimax action from the current game_state using
          self.depth and self.evaluationFunction.

        Here are some method calls that are useful when implementing minimax.

        game_state.getLegalActions(agent):
            Returns a list of legal actions for an agent
            agent=0 means Pacman, ghosts are >= 1

        game_state.generateSuccessor(agent, action):
            Returns the successor game state after an agent takes an action

        game_state.getNumAgents():
            Returns the total number of agents in the game

        game_state.isWin():  Returns True if this is a terminal winning state

        game_state.isLose():  Returns True if this is a terminal losing state


        """
        "*** YOUR CODE HERE ***"
        legalActions =  game_state.getLegalActions(0)
        best_value = float("-inf")
        best_action = None

        for eachAction in legalActions:
            successor_state = game_state.generateSuccessor(0, eachAction)
            successor_value = self.value(successor_state, 1, 1)#state, agent, depth
            if successor_value > best_value:
                best_value = successor_value
                best_action = eachAction
        return best_action


    def value(self, game_state, agent, current_depth):
        """ Returns the minimax value of any state"""
        "*** YOUR CODE HERE ***"
        win = game_state.isWin()
        loss = game_state.isLose()

        if win or loss or current_depth > self.depth:
            return self.evaluationFunction(game_state)
        if (agent == 0):
            return self.max_value(game_state, current_depth)
        else:
            return self.min_value(game_state, agent, current_depth)


    def max_value(self, game_state, current_depth):
        """Returns the minimax value of a state under Pacman's control (max)"""
        "*** YOUR CODE HERE ***"
        v = float("-inf")
        legalActions = game_state.getLegalActions(0)

        for eachAction in legalActions:
            successor_state = game_state.generateSuccessor(0, eachAction)
            successor_value = self.value(successor_state, 1, current_depth)  # state, agent, depth
            if successor_value > v:
                v = successor_value

        return v


    def min_value(self, game_state, agent, current_depth):
        """Returns the minimax value of a state under a ghost's control (min)"""
        "*** YOUR CODE HERE ***"
        v = float("inf")
        legalActions = game_state.getLegalActions(agent)
        total_agents = game_state.getNumAgents()

        if agent >= total_agents - 1:
            next_agent = 0
            current_depth += 1
        else:
            next_agent = agent + 1

        for eachAction in legalActions:
            successor_state = game_state.generateSuccessor(agent, eachAction)
            successor_value = self.value(successor_state, next_agent, current_depth)

            if successor_value < v:
                v = successor_value

        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, game_state):
        """
        Returns the best minimax action from the current game_state using
          self.depth and self.evaluationFunction.
        """
        "*** YOUR CODE HERE ***"
        legalActions = game_state.getLegalActions(0)
        best_value = float("-inf")
        best_action = None
        alpha = float("-inf")
        beta = float("inf")

        for eachAction in legalActions:
            successor_state = game_state.generateSuccessor(0, eachAction)
            successor_value = self.value(successor_state, 1, self.depth, alpha, beta)
            if successor_value > best_value:
                best_value = successor_value
                best_action = eachAction
            alpha = max(alpha, successor_value)
        return best_action

    def value(self, game_state, agent, current_depth, alpha, beta):
        """ Returns the minimax value of any state"""
        "*** YOUR CODE HERE ***"
        win = game_state.isWin()
        loss = game_state.isLose()

        if win or loss or current_depth == 0:
            return self.evaluationFunction(game_state)
        if (agent == 0):
            return self.max_value(game_state, current_depth, alpha, beta)
        else:
            return self.min_value(game_state, agent, current_depth, alpha, beta)

    def max_value(self, game_state, current_depth, alpha, beta):
        """Returns the minimax value of a state under Pacman's control (max)"""
        "*** YOUR CODE HERE ***"
        v = float("-inf")
        legalActions = game_state.getLegalActions(0)

        for eachAction in legalActions:
            successor_state = game_state.generateSuccessor(0, eachAction)
            v = max(v, self.value(successor_state, 1, current_depth, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, game_state, agent, current_depth, alpha, beta):
        """Returns the minimax value of a state under a ghost's control (min)"""
        "*** YOUR CODE HERE ***"
        v = float("inf")
        legalActions = game_state.getLegalActions(agent)
        total_agents = game_state.getNumAgents()
        next_agent = agent

        if agent == total_agents - 1:
            agent = 0
            current_depth -= 1
        else:
            agent = agent + 1

        for eachAction in game_state.getLegalActions(next_agent):
            successor_state = game_state.generateSuccessor(next_agent, eachAction)
            v = min(v, self.value(successor_state, agent, current_depth, alpha, beta))

            if v < alpha:
                return v
            beta = min(beta, v)
        return v

def betterEvaluationFunction(currentGameState):
    """
    This is not required.
    You can implement it if you like.
    You can test it by running:
    python pacman.py -p AlphaBetaAgent -a evalFn=better -l smallClassic
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
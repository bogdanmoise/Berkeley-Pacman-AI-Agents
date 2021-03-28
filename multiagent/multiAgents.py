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
import random, util

from game import Agent

class RandomAgent(Agent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        chosenAction = random.choice(legalMoves)
        return chosenAction

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newPoint = successorGameState.getCapsules()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        ghost_pos = currentGameState.getGhostPositions()
        food_list = newFood.asList()

        if len(food_list) == 0:
            return successorGameState.getScore()

        d1 = 0

        left_food = food_list[0]
        right_food = food_list[0]

        for food_1 in food_list:
            for food_2 in food_list:
                if(manhattanDistance(food_1, food_2) > d1):
                    d1 = manhattanDistance(food_1, food_2)
                    left_food = food_1
                    right_food = food_2
        
        dist_to_closest_food = d1 + min(manhattanDistance(newPos, left_food), manhattanDistance(newPos, right_food))
        dist_to_closest_ghost = min([(manhattanDistance(newPos, ghost)) for ghost in ghost_pos])

        if(dist_to_closest_ghost >= 2):
            dist_to_closest_ghost = 0
        else:
            dist_to_closest_ghost = - dist_to_closest_ghost
        return successorGameState.getScore() - dist_to_closest_food + dist_to_closest_ghost

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
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def max_value(self, gameState, depth):

            if(gameState.isWin() or gameState.isLose() or depth == self.depth):
                return self.evaluationFunction(gameState)

            legal_move = gameState.getLegalActions(0)
            max_point = -10000

            for move in legal_move:
                max_point = max(max_point, min_value(self, gameState.generateSuccessor(0, move), 1, depth))

            return max_point

        def min_value(self, gameState, agent_id, depth):

            if(gameState.isWin() or gameState.isLose() or depth == self.depth):
                return self.evaluationFunction(gameState)

            min_point = 10000

            if(agent_id < gameState.getNumAgents()):
                legal_move = gameState.getLegalActions(agent_id)
                for move in legal_move:
                    min_point = min(min_point, min_value(self, gameState.generateSuccessor(agent_id, move), agent_id + 1, depth))

                return min_point
            else:
                return max_value(self, gameState, depth + 1)


        legal_move = gameState.getLegalActions(0)
        max_score = -10000  
        next_move = Directions.STOP

        for move in legal_move:
            score = min_value(self, gameState.generateSuccessor(0, move), 1, 0)
            if (score > max_score):
                max_score = score
                next_move = move

        return next_move
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def max_value(self, gameState, depth, alpha, beta):

            if(gameState.isWin() or gameState.isLose() or depth == self.depth):
                return self.evaluationFunction(gameState)

            legal_move = gameState.getLegalActions(0)
            max_point = -10000

            for move in legal_move:
                max_point = max(max_point, min_value(self, gameState.generateSuccessor(0, move), 1, depth, alpha, beta))
                if(beta < max_point):
                    return max_point
                alpha = max(alpha, max_point)
            return max_point

        def min_value(self, gameState, agent_id, depth, alpha, beta):

            if(gameState.isWin() or gameState.isLose() or depth == self.depth):
                return self.evaluationFunction(gameState)

            min_point = 10000

            if(agent_id != gameState.getNumAgents()):
                legal_move = gameState.getLegalActions(agent_id)
                for move in legal_move:
                    min_point = min(min_point, min_value(self, gameState.generateSuccessor(agent_id, move), agent_id + 1, depth, alpha, beta))
                    if(alpha > min_point):
                        return min_point
                    beta = min(min_point, beta)
                return min_point
            else:
                return max_value(self, gameState, depth + 1, alpha, beta)


        legal_move = gameState.getLegalActions(0)
        max_score = -10000  
        next_move = Directions.STOP
        alpha = -10000
        beta = 10000

        for move in legal_move:
            score = min_value(self, gameState.generateSuccessor(0, move), 1, 0, alpha, beta)
            if (score > max_score):
                max_score = score
                next_move = move
            alpha = max(alpha, max_score)
        return next_move

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def max_value(self, gameState, depth):

            if(gameState.isWin() or gameState.isLose() or depth == self.depth):
                return self.evaluationFunction(gameState)

            legal_move = gameState.getLegalActions(0)
            max_point = -10000

            for move in legal_move:
                max_point = max(max_point, min_value(self, gameState.generateSuccessor(0, move), 1, depth))

            return max_point

        def min_value(self, gameState, agent_id, depth):

            if(gameState.isWin() or gameState.isLose() or depth == self.depth):
                return self.evaluationFunction(gameState)

            min_point = 10000
            s = 0.0

            if(agent_id < gameState.getNumAgents()):
                legal_move = gameState.getLegalActions(agent_id)

                for move in legal_move:
                    s = s + min_value(self, gameState.generateSuccessor(agent_id, move), agent_id + 1, depth)

                return (s / len(legal_move))
            else:
                return max_value(self, gameState, depth + 1)


        legal_move = gameState.getLegalActions(0)
        max_score = -10000  
        next_move = Directions.STOP

        for move in legal_move:
            score = min_value(self, gameState.generateSuccessor(0, move), 1, 0)
            if (score > max_score):
                max_score = score
                next_move = move

        return next_move
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()


    ghost_pos = currentGameState.getGhostPositions()
    food_list = newFood.asList()

    if len(food_list) == 0:
        return currentGameState.getScore()

    d1 = 0

    left_food = food_list[0]
    right_food = food_list[0]

    for food_1 in food_list:
        for food_2 in food_list:
            if(manhattanDistance(food_1, food_2) > d1):
                d1 = manhattanDistance(food_1, food_2)
                left_food = food_1
                right_food = food_2
    
    dist_to_closest_food = d1 + min(manhattanDistance(newPos, left_food), manhattanDistance(newPos, right_food))
    dist_to_closest_ghost = min([(manhattanDistance(newPos, ghost)) for ghost in ghost_pos])

    if(dist_to_closest_ghost > 2):
        dist_to_closest_ghost = 0
    else:
        dist_to_closest_ghost = 2
    return currentGameState.getScore() - dist_to_closest_food + dist_to_closest_ghost


    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

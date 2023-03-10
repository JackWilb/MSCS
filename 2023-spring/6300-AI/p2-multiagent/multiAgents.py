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
        newScore = successorGameState.getScore()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        sumNewFood = successorGameState.getNumFood()

        "*** YOUR CODE HERE ***"
        oldPos = currentGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        oldScore = currentGameState.getScore()
        oldGhostStates = currentGameState.getGhostStates()
        oldScaredTimes = [ghostState.scaredTimer for ghostState in oldGhostStates]
        sumOldFood = currentGameState.getNumFood()

        distanceToNearFood = min([util.manhattanDistance(newPos, pos) for pos in newFood.asList()]) if newFood.asList() else 0
        minScareTime = min(newScaredTimes)

        if action == 'Stop':
            return -1

        if oldPos == newPos:
            return -10

        return (1/(distanceToNearFood+1)) + (1/(sumNewFood + 1))+ (5/(minScareTime + 1)) + newScore - oldScore

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

        def minimaxRecur(state, index, depth):
            possibleActions = state.getLegalActions(index)
            currentBestAction = None

            # Recursion base case (game is over)
            if (state.isLose() or state.isWin() or depth == self.depth):
                return self.evaluationFunction(state), currentBestAction

            # If we're on the last ghost, increment the depth. Set index
            if index == state.getNumAgents() - 1:
                depth += 1
                nextIndex = self.index
            else:
                nextIndex = index + 1

            # Max / PacMan
            if index == 0:
                currentMax = -float("inf")

                for action in possibleActions:
                    successorState = state.generateSuccessor(index, action)
                    newMax = minimaxRecur(successorState, nextIndex, depth)[0]

                    if newMax > currentMax:
                        currentMax = newMax
                        currentBestAction = action

                return currentMax, currentBestAction
            # Min / ghosts
            else:
                currentMin = float("inf")

                for action in possibleActions:
                    successorState = state.generateSuccessor(index, action)
                    newMin = minimaxRecur(successorState, nextIndex, depth)[0]

                    if newMin < currentMin:
                        currentMin = newMin
                        currentBestAction = action
                
                return currentMin, currentBestAction
        
        return minimaxRecur(gameState, self.index, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphaBetaRecur(state, index, depth, alpha, beta):
            possibleActions = state.getLegalActions(index)
            currentBestAction = None

            # Recursion base case (game is over)
            if (state.isLose() or state.isWin() or depth == self.depth):
                return self.evaluationFunction(state), currentBestAction

            # If we're on the last ghost, increment the depth. Set index
            if index == state.getNumAgents() - 1:
                depth += 1
                nextIndex = self.index
            else:
                nextIndex = index + 1

            # Max / PacMan
            if index == 0:
                currentMax = -float("inf")
                
                for action in possibleActions:
                    successorState = state.generateSuccessor(index, action)
                    newVal = alphaBetaRecur(successorState, nextIndex, depth, alpha, beta)[0]

                    if max(currentMax, newVal) == newVal:
                        currentMax = newVal
                        currentBestAction = action

                    if currentMax > beta:
                        return currentMax, currentBestAction
                    alpha = max(currentMax, alpha)

                return currentMax, currentBestAction
            # Min / ghosts
            else:
                currentMin = float("inf")

                for action in possibleActions:
                    successorState = state.generateSuccessor(index, action)
                    newVal = alphaBetaRecur(successorState, nextIndex, depth, alpha, beta)[0]

                    if min(currentMin, newVal) == newVal:
                        currentMin = newVal
                        currentBestAction = action

                    if currentMin < alpha:
                        return currentMin, currentBestAction
                    beta = min(currentMin, beta)
                
                return currentMin, currentBestAction
        
        return alphaBetaRecur(gameState, self.index, 0, -float("inf"), float("inf"))[1]

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
        def expectimaxRecur(state, index, depth):
            possibleActions = state.getLegalActions(index)
            currentBestAction = None

            if (state.isLose() or state.isWin() or depth == self.depth):
                return self.evaluationFunction(state), currentBestAction

            # If we're on the last ghost, increment the depth. Set index
            if index == state.getNumAgents() - 1:
                depth += 1
                nextIndex = self.index
            else:
                nextIndex = index + 1

            if index != 0:
                prob = 1.0 / float(len(possibleActions))
                value = 0.0
                for action in possibleActions:
                    successorState = state.generateSuccessor(index, action)
                    expVal = expectimaxRecur(successorState, nextIndex, depth)[0]
                    value += prob * expVal
                return value, currentBestAction

            currentMax = -float("inf")
            for action in possibleActions:
                successorState = state.generateSuccessor(index, action)
                expVal = expectimaxRecur(successorState, nextIndex, depth)[0]
                
                if max(currentMax, expVal) == expVal:
                    currentMax, currentBestAction = expVal, action
                
            return currentMax, currentBestAction

        return expectimaxRecur(gameState, self.index, 0)[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    winningState = 1000 if currentGameState.isWin() else 0
    losingState = -1000 if currentGameState.isLose() else 0
    
    score = 1000 * currentGameState.getScore()
    
    pacmanPosition = currentGameState.getPacmanPosition()
    numFood = currentGameState.getNumFood()
    foodScore = 0
    for food in currentGameState.getFood().asList():
        foodScore += 1/(manhattanDistance(pacmanPosition, food)) * numFood

    return winningState + losingState + score + foodScore

# Abbreviation
better = betterEvaluationFunction

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodPos = newFood.asList ()
        foodCount = len (foodPos)
        closestDistance = 1e6
        for i in xrange (foodCount):
            distance = manhattanDistance (foodPos[i], newPos) + foodCount * 100
            if distance < closestDistance:
                closestDistance = distance
                #closestFood = foodPos
        if foodCount == 0:
            closestDistance = 0
        score = -closestDistance

        for i in xrange (len (newGhostStates)):
            ghostPos = successorGameState.getGhostPosition (i + 1)
            if manhattanDistance (newPos, ghostPos) <= 1:
                score -= 1e6
        return score
        #return successorGameState.getScore()

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
        """
        "*** YOUR CODE HERE ***"

        numAgent = gameState.getNumAgents ()
        ActionScore = []

        def rmStop(List):
            return [x for x in List if x != 'Stop']

        def miniMax(s, iterCount):
            if iterCount >= self.depth * numAgent or s.isWin () or s.isLose ():
                return self.evaluationFunction (s)
            if iterCount % numAgent != 0:  # Ghost min
                result = 1e10
                for a in rmStop (s.getLegalActions (iterCount % numAgent)):
                    sdot = s.generateSuccessor (iterCount % numAgent, a)
                    result = min (result, miniMax (sdot, iterCount + 1))
                return result
            else:  # Pacman Max
                result = -1e10
                for a in rmStop (s.getLegalActions (iterCount % numAgent)):
                    sdot = s.generateSuccessor (iterCount % numAgent, a)
                    result = max (result, miniMax (sdot, iterCount + 1))
                    if iterCount == 0:
                        ActionScore.append (result)
                return result

        result = miniMax (gameState, 0);
        # print _rmStop(gameState.getLegalActions(0)), ActionScore
        return rmStop (gameState.getLegalActions (0))[ActionScore.index (max (ActionScore))]



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      An expectimax agent you can use or modify
    """
    def expectimax_value (self, gameState, agentIndex, nodeDepth):
        if(agentIndex >= gameState.getNumAgents()):
            agentIndex = 0
            nodeDepth += 1	
        if( nodeDepth == self.depth ):
            return self.evaluationFunction(gameState)
        if( agentIndex == self.index ):
            return self.max_value(gameState, agentIndex, nodeDepth)        
      
        else:
            return self.exp_value(gameState, agentIndex, nodeDepth)
        
        return 'None'

    def max_value (self, gameState, agentIndex, nodeDepth):
      if( gameState.isWin() or gameState.isLose() ):
        return self.evaluationFunction(gameState)

      value = float("-inf")
      actionValue = "Stop"

      for legalActions in gameState.getLegalActions(agentIndex) :
        if legalActions == Directions.STOP:
          continue
        successor = gameState.generateSuccessor(agentIndex, legalActions)
        temp = self.expectimax_value(successor, agentIndex+1, nodeDepth)
        if( temp > value):
          value = temp
          actionValue = legalActions

      if( nodeDepth == 0 ):
        return actionValue
      else:
        return value

    def exp_value(self, gameState, agentIndex, nodeDepth):
      if( gameState.isWin() or gameState.isLose() ):
        return self.evaluationFunction(gameState)
      value = 0
      pr = 1.0/len(gameState.getLegalActions(agentIndex))
      
      for legalActions in gameState.getLegalActions(agentIndex):
        if( legalActions == Directions.STOP):
          continue
        successor = gameState.generateSuccessor(agentIndex, legalActions)
        value = value + (self.expectimax_value(successor, agentIndex+1, nodeDepth) * pr)
      return value

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        return self.expectimax_value(gameState,0,0)    
    

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 3). 

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    def scoreFromGhost(gameState):
      score = 0
      for ghost in gameState.getGhostStates():
        disGhost = manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition())
        if ghost.scaredTimer > 0:
          score += pow(max(8 - disGhost, 0), 2)
        else:
          score -= pow(max(7 - disGhost, 0), 2)
      return score

    def scoreFromFood(gameState):
      disFood = []
      for food in gameState.getFood().asList():
        disFood.append(1.0/manhattanDistance(gameState.getPacmanPosition(), food))
      if len(disFood)>0:
        return max(disFood)
      else:
        return 0

    def scoreFromCapsules(gameState):
      score = []
      for Cap in gameState.getCapsules():
        score.append(50.0/manhattanDistance(gameState.getPacmanPosition(), Cap))
      if len(score) > 0:
        return max(score)
      else:
        return 0

    score = currentGameState.getScore()
    scoreGhosts = scoreFromGhost(currentGameState)
    scoreFood = scoreFromFood(currentGameState)
    scoreCapsules = scoreFromCapsules(currentGameState)
    return score + scoreGhosts + scoreFood + scoreCapsules

# Abbreviation
better = betterEvaluationFunction


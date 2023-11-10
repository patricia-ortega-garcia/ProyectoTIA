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


import random

import util
from game import Agent
from util import manhattanDistance


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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        listaDistComidas =  []
        listaDistFantasma = []
        listaComidas = newFood.asList()
        puntuacion = 0
        minDistC = 1  
        minDistF = 1
        puntuacionSucesor = successorGameState.getScore()
        
        if successorGameState.isWin():
            puntuacion = 1000000


        if len(listaComidas)>0: 
            for comida in listaComidas:
                distComida = util.manhattanDistance(newPos,comida)
                listaDistComidas.append(distComida)

            minDistC = min(listaDistComidas)  #Comida más cercana al pacman
        
        """
        if len(newGhostStates)>0: 
            for fantasma in newGhostStates:
                distFan = util.manhattanDistance(newPos, fantasma.getPosition()) # posicion del fantasma con el pacman
                listaDistFantasma.append(distFan)
            
            minDistF = min(listaDistFantasma)   #Fantasma más cercano al pacman
        """
        if len(newGhostStates)>0: 
            distFan = 10000
            for fantasma in newGhostStates:
                distFanAct = util.manhattanDistance(newPos, fantasma.getPosition()) # posicion del fantasma con el pacman
                if distFanAct < distFan:
                        minDistF = distFanAct
                        fantasmaElegido = fantasma
            
        puntuacion = puntuacionSucesor + ((1/minDistC) * minDistF)
        if minDistF < 2 and fantasmaElegido.scaredTimer == 0:
            puntuacion = puntuacion - 10000 
    
        
        
        return puntuacion


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        super().__init__()
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, game_state):
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
        #[0] devuelve el score
        #[1] devuelve la action
        agentIndex = 0
        profundidadAct = 0
        profundidad = self.depth
        accion = self.value(game_state, agentIndex, profundidad)[1] #[1] devuelve la action
        return accion
    
    def value(self, game_state, agentIndex, profundidad):
        if game_state.isWin() or game_state.isLose() or profundidad == 0:
            return (self.evaluationFunction(game_state), "Stop") 
        elif agentIndex == 0:
            return self.maxValue(game_state, agentIndex, profundidad)
        elif agentIndex >= 1:
            return self.minValue(game_state, agentIndex, profundidad)
        
    def maxValue(self, game_state, agentIndex, profundidad):
        v = float("-inf")
        accionElegida = "Stop"

        listaAcciones = game_state.getLegalActions(agentIndex)
        nuevoAgente, nuevaProfundidad = self.actualizarVars(game_state, agentIndex, profundidad)
        
        for accion in listaAcciones:
            vNuevo = self.value(game_state.generateSuccessor(agentIndex, accion), nuevoAgente, nuevaProfundidad)[0] #[0] devuelve el score
            if vNuevo > v:
                v = vNuevo
                accionElegida = accion
        
        return (v, accionElegida)
    

    def minValue(self, game_state, agentIndex, profundidad):
        v = float("inf")
        accionElegida = "Stop"

        listaAcciones = game_state.getLegalActions(agentIndex)
        nuevoAgente, nuevaProfundidad = self.actualizarVars(game_state, agentIndex, profundidad)

        for accion in listaAcciones:
            vNuevo = self.value(game_state.generateSuccessor(agentIndex, accion), nuevoAgente, nuevaProfundidad)[0] #[0] devuelve el score
            if vNuevo < v:
                v = vNuevo
                accionElegida = accion
        
        return (v, accionElegida)
    
    def actualizarVars(self, game_state, agentIndex, profundidad):
        numAgente = game_state.getNumAgents()

        if agentIndex == numAgente-1:           #Cuando ya haya sido el turno de todos los agentes
            nuevoAgente = 0
            nuevaProfundidad = profundidad-1
        else:
            nuevoAgente = agentIndex+1
            nuevaProfundidad = profundidad
        return nuevoAgente, nuevaProfundidad
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        #[0] devuelve el score
        #[1] devuelve la action
        agentIndex = 0
        profundidadAct = 0
        profundidad = self.depth
        accion = self.valueAlphaBeta(game_state, agentIndex, profundidad)[1] #[1] devuelve la action
        return accion
    
    def valueAlphaBeta(self, game_state, agentIndex, profundidad, alpha = float('-inf'), beta = float('inf')):

        if game_state.isWin() or game_state.isLose() or profundidad == 0:
            return (self.evaluationFunction(game_state), "Stop") 
        elif agentIndex == 0:
            return self.maxValue(game_state, agentIndex, profundidad, alpha, beta)
        elif agentIndex >= 1:
            return self.minValue(game_state, agentIndex, profundidad, alpha, beta)
        
    def maxValue(self, game_state, agentIndex, profundidad, alpha, beta):
        v = float("-inf")
        accionElegida = "Stop"

        listaAcciones = game_state.getLegalActions(agentIndex)
        nuevoAgente, nuevaProfundidad = self.actualizarVars(game_state, agentIndex, profundidad)
        
        for accion in listaAcciones:
            vNuevo = self.valueAlphaBeta(game_state.generateSuccessor(agentIndex, accion), nuevoAgente, nuevaProfundidad, alpha, beta)[0] #[0] devuelve el score
            if vNuevo > v:
                v = vNuevo
                accionElegida = accion
            if vNuevo > beta:
                return (vNuevo, accionElegida)
            
            alpha = max(alpha, vNuevo)
        
        return (v, accionElegida)
    

    def minValue(self, game_state, agentIndex, profundidad, alpha, beta):
        v = float("inf")
        accionElegida = "Stop"

        listaAcciones = game_state.getLegalActions(agentIndex)
        nuevoAgente, nuevaProfundidad = self.actualizarVars(game_state, agentIndex, profundidad)

        for accion in listaAcciones:
            vNuevo = self.valueAlphaBeta(game_state.generateSuccessor(agentIndex, accion), nuevoAgente, nuevaProfundidad, alpha, beta)[0] #[0] devuelve el score
            if vNuevo < v:
                v = vNuevo
                accionElegida = accion
            if vNuevo < alpha:
                return (vNuevo, accionElegida)
            
            beta = min(beta, vNuevo)
        
        return (v, accionElegida)
    
    def actualizarVars(self, game_state, agentIndex, profundidad):
        numAgente = game_state.getNumAgents()

        if agentIndex == numAgente-1:           #Cuando ya haya sido el turno de todos los agentes
            nuevoAgente = 0
            nuevaProfundidad = profundidad-1
        else:
            nuevoAgente = agentIndex+1
            nuevaProfundidad = profundidad
        return nuevoAgente, nuevaProfundidad



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
        #util.raiseNotDefined()
        agentIndex = 0
        profundidadAct = 0
        profundidad = self.depth
        accion = self.valueExpectimax(gameState, agentIndex, profundidad)[1] #[1] devuelve la action
        return accion

    def valueExpectimax(self, game_state, agentIndex, profundidad):

        if game_state.isWin() or game_state.isLose() or profundidad == 0:
            return (self.evaluationFunction(game_state), "Stop") 
        elif agentIndex == 0:
            return self.maxValue(game_state, agentIndex, profundidad)
        elif agentIndex >= 1:
            return self.expValue(game_state, agentIndex, profundidad) 
        

    def maxValue(self,game_state, agentIndex, profundidad):
        v = float("-inf")
        accionElegida = "Stop"
       
        listaAcciones = game_state.getLegalActions(agentIndex)
        nuevoAgente, nuevaProfundidad = self.actualizarVars(game_state, agentIndex, profundidad)
      

        for accion in listaAcciones:
            vNuevo = self.valueExpectimax(game_state.generateSuccessor(agentIndex, accion), nuevoAgente, nuevaProfundidad)[0] #[0] devuelve el score
            if vNuevo > v:
                v = vNuevo
                accionElegida = accion
        
        return (v, accionElegida)
    

    def expValue(self,game_state, agentIndex, profundidad):

        v = 0
        accionElegida = "Stop"
        vNuevo = 0

        listaAcciones = game_state.getLegalActions(agentIndex)
        nuevoAgente, nuevaProfundidad = self.actualizarVars(game_state, agentIndex, profundidad)

        prob = 1 / float(len(listaAcciones)) # probabilidad uniforme en base al número de acciones.

        for accion in listaAcciones:
            vNuevo =  self.valueExpectimax(game_state.generateSuccessor(agentIndex, accion), nuevoAgente, nuevaProfundidad)[0]  #[0] devuelve el score
            accionElegida = accion
            v = v + (prob * vNuevo) # se va calculando la media de todas las acciones

        return (v, accionElegida)



    def actualizarVars(self, game_state, agentIndex, profundidad):
        numAgente = game_state.getNumAgents()

        if agentIndex == numAgente-1:           #Cuando ya haya sido el turno de todos los agentes
            nuevoAgente = 0
            nuevaProfundidad = profundidad-1
        else:
            nuevoAgente = agentIndex+1
            nuevaProfundidad = profundidad
        return nuevoAgente, nuevaProfundidad


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    pacman_pos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    minDistC = 1  
    minDistF = 1
    listaDistComidas =  []
    listaDistFantasma = []
    listaComidas = newFood.asList()
    pastillas = currentGameState.getCapsules()
    puntAct = currentGameState.getScore()
    numComidasRestantes = len(listaComidas)


    #Buscar la comida más cercana
    if len(listaComidas)>0: 
        for comida in listaComidas:
            distComida = util.manhattanDistance(pacman_pos,comida)
            listaDistComidas.append(distComida)

        minDistC = min(listaDistComidas)    #Comida más cercana al pacman


    #Buscar el fantasma más cercano
    """
    if len(newGhostStates)>0: 
        for fantasma in newGhostStates:
            distFan = util.manhattanDistance(pacman_pos, fantasma.getPosition()) # posicion del fantasma con el pacman
            listaDistFantasma.append(distFan)
        
        minDistF = min(listaDistFantasma)   #Fantasma más cercano al pacman
    """

    if len(newGhostStates)>0: 
        distFan = 10000
        for fantasma in newGhostStates:
            distFanAct = util.manhattanDistance(pacman_pos, fantasma.getPosition()) # posicion del fantasma con el pacman
            if distFanAct < distFan:
                    minDistF = distFanAct
                    fantasmaElegido = fantasma
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~AJUSTAR PUNTUACIÓN~~~~~~~~~~~~~~~~~~~~~~~~~~

    #Cuanto más cerca de la Comida mejor, cuanto más lejos del fantasma mejor
    puntuacion = puntAct + ((1/minDistC) * minDistF)
    
    
    #Si muy cerca de un fantasma no asustado, muy malo
    if minDistF < 2 and fantasmaElegido.scaredTimer == 0:
        puntuacion = puntuacion - 10000 
    

    #Lo mejor que puede pasar es que ganes
    if currentGameState.isWin():
        puntuacion = 100000

    
    #Considerar el tiempo de invulneravilidad restante
    for tiempoAsustado in newScaredTimes:
        puntuacion = puntuacion + tiempoAsustado


    #Cuantas menos comidas queden por comer mejor
    if numComidasRestantes != 0:
        puntuacion = puntuacion + (1/numComidasRestantes)

    return puntuacion


# Abbreviation
better = betterEvaluationFunction

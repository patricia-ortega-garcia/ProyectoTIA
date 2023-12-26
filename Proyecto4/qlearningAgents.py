# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues o
        - computeActionFromQValues
        - getQValue o
        - getAction
        - update o

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.valoresQ = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        
        return self.valoresQ[(state, action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        valorMax = 0.0
        accionesLegales = self.getLegalActions(state)

        # Si no hay acciones legales (estado terminal) devolvemos 0.0
        if not accionesLegales:
          return valorMax

        
        # Mirar todas las acciones legales y obtener la que nos da mayor valor
        valsQ = []
        for accion in accionesLegales:
          valorNuevo = self.getQValue(state, accion)
          valsQ.append(valorNuevo)

        # Obtenemos la mayor Q 
        maxQ = max(valsQ)

        # Devolver maximo valor Q para el estado actual 
        return maxQ

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        accionesLegales = self.getLegalActions(state)

        # Si no hay acciones legales, devolver None
        if not accionesLegales:
          return None

        # Obtener valor Q para cada acción legal
        #valsQ = []
        #for accion in accionesLegales:
        #  valorNuevo = self.getQValue(state, accion)
        #  valsQ.append(valorNuevo)

        # Obtenemos la mayor Q 
        #maxQ = max(valsQ)
        maxQ = self.computeValueFromQValues(state)

        # Obtenemos las acciones correspondientes
        mejoresAcciones = []
        for accion in accionesLegales:
          valorQ = self.getQValue(state, accion)
          if valorQ == maxQ:
            mejoresAcciones.append(accion)

        # Si hay empates elegimos al azar
        return random.choice(mejoresAcciones)

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        # Si no hay acciones legales, devolver None
        if not legalActions:
            return None

        # Decide entre exploración y explotación
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)  # Exploración: elige una acción al azar
        else:
            return self.computeActionFromQValues(state)  # Explotación: elige la mejor acción conocida


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        alpha = self.alpha  # Tasa de aprendizaje
        descuento = self.discount  # Factor de descuento

        # Calcular nuevo valor Q utilizando la fórmula Q-learning
        valorMax = self.computeValueFromQValues(nextState)
        nuevoQ = (1 - alpha) * self.getQValue(state, action) + alpha * (reward + descuento * valorMax)

        # Actualiza valor Q para el estado y la acción actuales
        self.valoresQ[(state, action)] = nuevoQ

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        pesos = self.weights
        features = self.featExtractor.getFeatures(state,action) #sacar los rasgos que existen
        valorQ = 0 #inicializar valor Q
        
        for i in pesos:
            valorQ = valorQ + (features[i] * pesos[i]) #formula para actualizar Q
        
        return valorQ


    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        pesos = self.getWeights() #obtener pesos
        rasgos = self.featExtractor.getFeatures(state,action) #features para ese estado y accion
        valorQActual = self.getQValue(state,action) # valor q actual 
        qMax = self.computeValueFromQValues(nextState) #valor q maximo

        difference = (reward + (self.discount * qMax )) - valorQActual #diferencia entre q nuevo y q actual
        for rasgo in rasgos:
          pesos[rasgo] = pesos[rasgo] + self.alpha * difference * rasgos[rasgo]
    

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass

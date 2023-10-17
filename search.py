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

from abc import ABC, abstractmethod
#from util import Stack, PriorityQueue
import util
import heapq


class SearchProblem(ABC):
	"""
	This class outlines the structure of a search problem, but doesn't implement
	any of the methods (in object-oriented terminology: an abstract class).

	You do not need to change anything in this class, ever.
	"""

	@abstractmethod
	def getStartState(self):
		"""
		Returns the start state for the search problem.
		"""
		util.raiseNotDefined()

	@abstractmethod
	def isGoalState(self, state):
		"""
		  state: Search state

		Returns True if and only if the state is a valid goal state.
		"""
		util.raiseNotDefined()

	@abstractmethod
	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples, (successor,
		action, stepCost), where 'successor' is a successor to the current
		state, 'action' is the action required to get there, and 'stepCost' is
		the incremental cost of expanding to that successor.
		"""
		util.raiseNotDefined()

	@abstractmethod
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
	return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	"""
	"*** YOUR CODE HERE ***"
	print("SE ESTÁ USANDO EL MÉTODO depthFirstSearch")

	#print("Start:", problem.getStartState())
	#print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
	#print("Start's successors:", problem.getSuccessors(problem.getStartState()))
	
	nodoInicial = problem.getStartState()
	porVisitar = [(nodoInicial, [])] #Nodo y camino que indica como se llega hasta él
	visitados = []
	costeTotal = 0

	while porVisitar:
		print(porVisitar)
		nodoAct, camino_hasta_nodo = porVisitar.pop() #Nodo y camino que indica como se llega hasta él

		#print(str(camino_hasta_nodo))

		if nodoAct not in visitados:
			if problem.isGoalState(nodoAct):
				print("¡Hemos llegado al objetivo!")
				print("Las direcciones que tenemos que tomar hasta la comida son las siguientes: ")
				print(str(camino_hasta_nodo))

				print("Y el coste total del camino es: ")
				print(str(costeTotal))
				
				return camino_hasta_nodo

			else:
				visitados.append(nodoAct)
				for nodoSucesor, direcSucesor, costeSucesor in problem.getSuccessors(nodoAct):
					nuevoCamino = camino_hasta_nodo + [direcSucesor]
					nuevoNodo = (nodoSucesor, nuevoCamino)
					costeTotal = costeTotal + costeSucesor # NO LO DEVUELVE BIEN
					if nodoSucesor not in visitados:
						porVisitar.append(nuevoNodo)  # Agregar el nodo sucesor y su camino

	return camino_hasta_nodo
	#util.raiseNotDefined()

def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""
	"*** YOUR CODE HERE ***"
	print("SE ESTÁ USANDO EL MÉTODO breadthFirstSearch")
	
	nodoInicial = problem.getStartState()
	porVisitar = [(nodoInicial, [])] #Nodo y camino que indica como se llega hasta él
	visitados = []
	costeTotal = 0

	#prueba de github 2 :D
	# ffff

	while porVisitar:
		#print(porVisitar)
		nodoAct, camino_hasta_nodo = porVisitar.pop(0) #Nodo y camino que indica como se llega hasta él

		#print(str(camino_hasta_nodo))

		if nodoAct not in visitados:
			if problem.isGoalState(nodoAct):
				print("¡Hemos llegado al objetivo!")
				print("Las direcciones que tenemos que tomar hasta la comida son las siguientes: ")
				print(str(camino_hasta_nodo))

				print("Y el coste total del camino es: ")
				print(str(costeTotal))
				
				return camino_hasta_nodo

			else:
				visitados.append(nodoAct)
				for nodoSucesor, direcSucesor, costeSucesor in problem.getSuccessors(nodoAct):
					nuevoCamino = camino_hasta_nodo + [direcSucesor]
					nuevoNodo = (nodoSucesor, nuevoCamino)
					costeTotal = costeTotal + costeSucesor # NO LO DEVUELVE BIEN
					if nodoSucesor not in visitados:
						porVisitar.append(nuevoNodo)  # Agregar el nodo sucesor y su camino

	return camino_hasta_nodo
	#util.raiseNotDefined()


def uniformCostSearch(problem):
	"""Search the node of least total cost first."""
	"""
	#VERSION 1 DEL CODIGO
	print("SE ESTÁ USANDO EL MÉTODO uniformCostSearch")

	nodoInicial = problem.getStartState()
	porVisitar = [(0, nodoInicial, [])] #Tupla: coste acumuado, nodo, camino hasta el nodo
	visitados = []
	while porVisitar:
		costeAcum, nodoAct, camino_hasta_nodo = heapq.heappop(porVisitar) #Nodo y camino que indica como se llega hasta él 
		if nodoAct not in visitados:
			if problem.isGoalState(nodoAct):
				print("¡Hemos llegado al objetivo!")
				print("Las direcciones que tenemos que tomar hasta la comida son las siguientes: ")
				print(camino_hasta_nodo)
				print("Y el coste total del camino es: ")
				print(costeAcum)
				return camino_hasta_nodo
			
			else: 
				visitados.append(nodoAct)
				for nodoSucesor, direcSucesor, costeSucesor in problem.getSuccessors(nodoAct):
					(nuevoCoste) = costeAcum + costeSucesor
					nuevoCamino = camino_hasta_nodo + [direcSucesor]
					if nodoSucesor not in visitados:
						heapq.heappush(porVisitar, (nuevoCoste, nodoSucesor, nuevoCamino))
	"""


	#VERSION FINAL DEL CODIGO
	print("SE ESTÁ USANDO EL MÉTODO uniforCostSearch")
	nodoInicial = problem.getStartState()
	visitados = []
	porVisitar = util.PriorityQueue() #Tupla: (nodo, camino hasta el nodo) costeAcumulado
	porVisitar.push((nodoInicial, []), 0)

	while porVisitar:
		nodoAct, camino_hasta_nodo = porVisitar.pop() #Nodo y camino que indica como se llega hasta él 
		if nodoAct not in visitados:
			if problem.isGoalState(nodoAct):
				print("¡Hemos llegado al objetivo!")
				print("Las direcciones que tenemos que tomar hasta la comida son las siguientes: ")
				print(camino_hasta_nodo)
				return camino_hasta_nodo
			
			else: 
				visitados.append(nodoAct)
				for nodoSucesor, direcSucesor, costeSucesor in problem.getSuccessors(nodoAct):
					nuevoCamino = camino_hasta_nodo + [direcSucesor]
					nuevoCoste = problem.getCostOfActions(nuevoCamino) + costeSucesor
					if nodoSucesor not in visitados:
						porVisitar.push((nodoSucesor, nuevoCamino), nuevoCoste)




def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0


def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	
	nodoInicial = problem.getStartState()
	porVisitar = util.PriorityQueue()
	porVisitar.push((0, nodoInicial, []),0) #(Tupla: coste acumuado, nodo, camino hasta el nodo), coste + heuristico
	visitados = []
	while porVisitar:
		
		costeAcum, nodoAct, camino_hasta_nodo = porVisitar.pop() #Nodo y camino que indica como se llega hasta él 
		if nodoAct not in visitados:
			
			if problem.isGoalState(nodoAct):
				print("¡Hemos llegado al objetivo!")
				print("Las direcciones que tenemos que tomar hasta la comida son las siguientes: ")
				print(camino_hasta_nodo)
				print("Y el coste total del camino es: ")
				print(costeAcum)
				return camino_hasta_nodo
			
			else: 
				visitados.append(nodoAct)
				for nodoSucesor, direcSucesor, costeSucesor in problem.getSuccessors(nodoAct):
					nuevoCoste = costeAcum + costeSucesor 
					costeHeuristico = nuevoCoste + heuristic(nodoSucesor,problem)
					nuevoCamino = camino_hasta_nodo + [direcSucesor]
					if nodoSucesor not in visitados:
						porVisitar.push((nuevoCoste, nodoSucesor, nuevoCamino), costeHeuristico)
						#heapq.heappush(porVisitar, (costeHeuristico, nuevoCoste, nodoSucesor, nuevoCamino)) utilizado en la anterior versión del código.



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

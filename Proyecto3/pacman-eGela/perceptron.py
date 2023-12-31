# perceptron.py
# -------------
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



import time
import util

PRINT = True


# Perceptron implementation

class PerceptronClassifier:
    """
    Perceptron classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """

    def __init__(self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "perceptron"
        self.max_iterations = max_iterations
        self.weights = {}
        self.features = None
        for label in legalLabels:
            self.weights[label] = util.Counter()  # this is the data-structure you should use

    def setWeights(self, weights):
        assert len(weights) == len(self.legalLabels)
        self.weights = weights

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        The training loop for the perceptron passes through the training data several
        times and updates the weight vector for each label based on classification errors.
        See the project description for details.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        (and thus represents a vector a values).
        """

        self.features = trainingData[0].keys()  # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.
        label = util.Counter() # 
        for iteration in range(self.max_iterations):
            print("Starting iteration ", iteration, "...")
            for i in range(len(trainingData)):  # training data
                #print(trainingData[i]) # esto es un break point para que puedas comprobar el formato de los datos
                ########################################################################################
                # 1. i es el indice de un ejemplo (un item, f(x) de un ejemplo) del conjunto de entrenamiento.
                # 2. Asi pues, en cada vuelta de este loop se trata un solo ejemplo
                #    por cada ejemplo calculareis el producto punto (dotProduct) w*item
                #    NOTAS: Recordad que cada ejemplo viene representado por varios rasgos (o features), es decir, es un vector de rasgos, tantos como nos marca el atributo self.features.
                #          Asi cada ejemplo es de dimension 1 filas y self.features).
                #          La dimension del vector w tambien es self.features, es decir, habra tantos pesos en w_rasgo dentro de w como rasgos haya en cada item de ejemplo
                #          Recordad tambien que es una clasificacion multiclase en este caso. Hay tantas clases como nos marca el atributo self.legalLabels
                #########################################################################################
                "*** YOUR CODE HERE ***"
                for j in self.legalLabels:
                    print("J y peso:  "  + str(self.weights[j]))
                    label[j] = trainingData[i].__mul__(self.weights[j])
                if trainingLabels[i] != label.argMax(): # y prima es label.argMax(), si la etiqueta del ejemplo no coincide con la etiqueta que da el producto
                    self.weights[trainingLabels[i]] += trainingData[i]  # le damos mas peso
                    self.weights[label.argMax()] -= trainingData[i]     # le damos menos peso
                #  util.raiseNotDefined()

    def classify(self, data):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for label in self.legalLabels:
                vectors[label] = self.weights[label] * datum
            guesses.append(vectors.argMax())
        return guesses

    def findHighWeightFeatures(self, label):
        """
        Returns a list of the 100 features with the greatest weight for some label
        """
        featuresWeights = []

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

        return featuresWeights

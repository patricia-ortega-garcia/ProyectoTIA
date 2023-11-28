import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.
        
        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        Deberiais obtener el producto escalar (o producto punto) que es "equivalente" a la distancia del coseno
        """
        "*** YOUR CODE HERE ***"
        pesos = self.get_weights()
        escalar = nn.DotProduct(x, pesos)
        return escalar


    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.
        Dependiendo del valor del coseno devolvera 1 o -1
        
        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        valorEnScalar = self.run(x)
        valorEnFloat = nn.as_scalar(valorEnScalar)

        if valorEnFloat < 0:
            return -1   #Si es negativo devuelve -1
        else: 
            return 1    #Si no es negativo devuelve 1


    def train(self, dataset):
        """
        Train the perceptron until convergence.
        Hasta que TODOS los ejemplos del train esten bien clasificados. Es decir, hasta que la clase predicha en se corresponda con la real en TODOS los ejemplos del train
        """
        "*** YOUR CODE HERE ***"
        convergencia = False
        while not convergencia:
            convergencia = True

            for iteracion in dataset.iterate_once(1):    #Se dan vueltas al conjunto de datos.En el momento en el que no haya cambios, saldremos de la iteración (converg alcanzada)
                
                prediccAct = self.get_prediction(iteracion[0])
                realAct = nn.as_scalar(iteracion[1])

                if prediccAct != realAct: 
                    convergencia = False
                    nn.Parameter.update(self.get_weights(),iteracion[0],realAct)




class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    NO ES CLASIFICACION, ES REGRESION. ES DECIR; APRENDER UNA FUNCION.
    SI ME DAN X TENGO QUE APRENDER A OBTENER LA MISMA Y QUE EN LA FUNCION ORIGINAL DE LA QUE QUIERO APRENDER
    """
    def __init__(self):
        # Initialize your model parameters here
        # For example:
        # self.batch_size = 20
        # self.w0 = nn.Parameter(1, 5)
        # self.b0 = nn.Parameter(1, 5)
        # self.w1 = nn.Parameter(5, 1)
        # self.b1 = nn.Parameter(1, 1)
        # self.lr = -0.01
        #
        "*** YOUR CODE HERE ***"
        self.batch_size = 20
        self.w0 = nn.Parameter(1, 50)
        self.b0 = nn.Parameter(1, 50)
        self.w1 = nn.Parameter(50, 1)
        self.b1 = nn.Parameter(1, 1)
        self.lr = -0.005
        self.fb = nn.Parameter(1,15)
        self.sb = nn.Parameter(1,10)
        self.tw = nn.Parameter(10,1)
        self.tb = nn.Parameter(1,1)
        self.learning_rate = -0.005





    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1). En este caso cada ejemplo solo esta compuesto por un rasgo
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values.
            Como es un modelo de regresion, cada valor y tambien tendra un unico valor
        """
        "*** YOUR CODE HERE ***"
        escondido = nn.ReLU(nn.AddBias(nn.Linear(x, self.w0), self.b0))
        operacion = nn.AddBias(nn.Linear(escondido, self.w1), self.b1)
        print("La OPERACION ES: ", operacion)
        return operacion






    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
                ----> ES FACIL COPIA Y PEGA ESTO Y ANNADE LA VARIABLE QUE HACE FALTA PARA CALCULAR EL ERROR 
                return nn.SquareLoss(self.run(x),ANNADE LA VARIABLE QUE ES NECESARIA AQUI), para medir el error, necesitas comparar el resultado de tu prediccion con .... que?
        """
        "*** YOUR CODE HERE ***"
        predicho = self.run(x) # valor predicho
        error = nn.SquareLoss(predicho,y) # calculo del error
        return error






    def train(self, dataset):
        """
        Trains the model.
        
        """
        
        batch_size = self.batch_size
        total_loss = 100000
        #while total_loss > 0.02:
        while total_loss > 0.03:
            #ITERAR SOBRE EL TRAIN EN LOTES MARCADOS POR EL BATCH SIZE COMO HABEIS HECHO EN LOS OTROS EJERCICIOS
            #ACTUALIZAR LOS PESOS EN BASE AL ERROR loss = self.get_loss(x, y) QUE RECORDAD QUE GENERA
            #UNA FUNCION DE LA LA CUAL SE  PUEDE CALCULAR LA DERIVADA (GRADIENTE)

            "*** YOUR CODE HERE ***"
            for x, y in dataset.iterate_forever(batch_size):
                error = self.get_loss(x, y)
                gradients = nn.gradients(error, [self.w0, self.b0, self.w1, self.b1])

                self.w0.update(gradients[0], -self.lr)
                self.b0.update(gradients[1], -self.lr)
                self.w1.update(gradients[2], -self.lr)
                self.b1.update(gradients[3], -self.lr)

            total_loss = nn.as_scalar(error)





            
class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        # TEN ENCUENTA QUE TIENES 10 CLASES, ASI QUE LA ULTIMA CAPA TENDRA UNA SALIDA DE 10 VALORES,
        # UN VALOR POR CADA CLASE

        output_size = 10 # TAMANO EQUIVALENTE AL NUMERO DE CLASES DADO QUE QUIERES OBTENER 10 CLASES
        pixel_dim_size = 28
        pixel_vector_length = pixel_dim_size* pixel_dim_size
 
        "*** YOUR CODE HERE ***"

     

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
            output_size = 10 # TAMANO EQUIVALENTE AL NUMERO DE CLASES DADO QUE QUIERES OBTENER 10 "COSENOS"
        """
        "*** YOUR CODE HERE ***"





    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).
        POR EJEMPLO: [0,0,0,0,0,1,0,0,0,0,0] seria la y correspondiente al 5
                     [0,1,0,0,0,0,0,0,0,0,0] seria la y correspondiente al 1

        EN ESTE CASO ESTAMOS HABLANDO DE MULTICLASS, ASI QUE TIENES QUE CALCULAR 
        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"#NO ES NECESARIO QUE LO IMPLEMENTEIS, SE OS DA HECHO
        return nn.SoftmaxLoss(self.run(x), y) # COMO VEIS LLAMA AL RUN PARA OBTENER POR CADA BATCH
                                              # LOS 10 VALORES DEL "COSENO". TENIENDO EL Y REAL POR CADA EJEMPLO
                                              # APLICA SOFTMAX PARA CALCULAR LA PROBABILIDA MAX
                                              # Y ESA SERA SU PREDICCION,
                                              # LA CLASE QUE MUESTRE EL MAYOR PROBABILIDAD, LA PREDICCION MAS PROBABLE, Y LUEGO LA COMPARARA CON Y 

    def train(self, dataset):
        """
        Trains the model.
        EN ESTE CASO EN VEZ DE PARAR CUANDO EL ERROR SEA MENOR QUE UN VALOR O NO HAYA ERROR (CONVERGENCIA),
        SE PUEDE HACER ALGO SIMILAR QUE ES EN NUMERO DE ACIERTOS. EL VALIDATION ACCURACY
        NO LO TENEIS QUE IMPLEMENTAR, PERO SABED QUE EMPLEA EL RESULTADO DEL SOFTMAX PARA CALCULAR
        EL NUM DE EJEMPLOS DEL TRAIN QUE SE HAN CLASIFICADO CORRECTAMENTE 
        """
        batch_size = self.batch_size
        while dataset.get_validation_accuracy() < 0.97:
            #ITERAR SOBRE EL TRAIN EN LOTES MARCADOS POR EL BATCH SIZE COMO HABEIS HECHO EN LOS OTROS EJERCICIOS
            #ACTUALIZAR LOS PESOS EN BASE AL ERROR loss = self.get_loss(x, y) QUE RECORDAD QUE GENERA
            #UNA FUNCION DE LA LA CUAL SE  PUEDE CALCULAR LA DERIVADA (GRADIENTE)
            "*** YOUR CODE HERE ***"





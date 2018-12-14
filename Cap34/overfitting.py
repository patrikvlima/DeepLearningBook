"""
Overfitting
~~~~~~~~~~~
Plots para ilustrar o problema do Overfitting. 
"""

# Imports
import json
import random
import sys
import matplotlib.pyplot as plt
import numpy as np

# Nossa biblioteca
sys.path.append('../src/')
import mnist_loader
import network2


def main(filename, num_epochs,
         training_cost_xmin=200, 
         test_accuracy_xmin=200, 
         test_cost_xmin=0, 
         training_accuracy_xmin=0,
         training_set_size=1000, 
         lmbda=0.0):
    """
    ``filename`` é o nome do arquivo onde os resultados serão armazenados.
    ``num_epochs`` é o número de épocas para treinar.
    ``training_set_size`` é o número de imagens para treinar.
    ``lmbda`` é o parâmetro de regularização.
    Os outros parâmetros definem as épocas nas quais começar a plotar no eixo x.
    """
    run_network(filename, num_epochs, training_set_size, lmbda)
    make_plots(filename, num_epochs, 
               training_cost_xmin,
               test_accuracy_xmin,
               test_cost_xmin, 
               training_accuracy_xmin,
               training_set_size)
                       
def run_network(filename, num_epochs, training_set_size=1000, lmbda=0.0):
    """Treina a rede para ``num_epochs`` em ``training_set_size``
     imagens e armazene os resultados em ``filename``. Esses resultados podem
     mais tarde ser usado por ``make_plots``. Note que os resultados são armazenados
     no disco em grande parte porque é conveniente não ter que
     ``run_network`` toda vez que quisermos fazer um gráfico (é lento).
    """
    # Torne os resultados mais facilmente reproduzíveis
    random.seed(12345678)
    np.random.seed(12345678)
    training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
    net = network2.Network([784, 30, 10], cost=network2.CrossEntropyCost())
    net.large_weight_initializer()
    test_cost, test_accuracy, training_cost, training_accuracy \
        = net.SGD(training_data[:training_set_size], num_epochs, 10, 0.5,
                  evaluation_data=test_data, lmbda = lmbda,
                  monitor_evaluation_cost=True, 
                  monitor_evaluation_accuracy=True, 
                  monitor_training_cost=True, 
                  monitor_training_accuracy=True)
    f = open(filename, "w")
    json.dump([test_cost, test_accuracy, training_cost, training_accuracy], f)
    f.close()

def make_plots(filename, num_epochs, 
               training_cost_xmin=200, 
               test_accuracy_xmin=200, 
               test_cost_xmin=0, 
               training_accuracy_xmin=0,
               training_set_size=1000):
    """Carregue os resultados de `` filename`` e gere as parcelas correspondente."""
    f = open(filename, "r")
    test_cost, test_accuracy, training_cost, training_accuracy = json.load(f)
    f.close()
    plot_training_cost(training_cost, num_epochs, training_cost_xmin)
    plot_test_accuracy(test_accuracy, num_epochs, test_accuracy_xmin)
    plot_test_cost(test_cost, num_epochs, test_cost_xmin)
    plot_training_accuracy(training_accuracy, num_epochs, 
                           training_accuracy_xmin, training_set_size)
    plot_overlay(test_accuracy, training_accuracy, num_epochs,
                 min(test_accuracy_xmin, training_accuracy_xmin),
                 training_set_size)

def plot_training_cost(training_cost, num_epochs, training_cost_xmin):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.arange(training_cost_xmin, num_epochs), 
            training_cost[training_cost_xmin:num_epochs],
            color='#2A6EA6')
    ax.set_xlim([training_cost_xmin, num_epochs])
    ax.grid(True)
    ax.set_xlabel('Epoch')
    ax.set_title('Cost on the training data')
    plt.show()

def plot_test_accuracy(test_accuracy, num_epochs, test_accuracy_xmin):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.arange(test_accuracy_xmin, num_epochs), 
            [accuracy/100.0 
             for accuracy in test_accuracy[test_accuracy_xmin:num_epochs]],
            color='#2A6EA6')
    ax.set_xlim([test_accuracy_xmin, num_epochs])
    ax.grid(True)
    ax.set_xlabel('Epoch')
    ax.set_title('Accuracy (%) on the test data')
    plt.show()

def plot_test_cost(test_cost, num_epochs, test_cost_xmin):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.arange(test_cost_xmin, num_epochs), 
            test_cost[test_cost_xmin:num_epochs],
            color='#2A6EA6')
    ax.set_xlim([test_cost_xmin, num_epochs])
    ax.grid(True)
    ax.set_xlabel('Epoch')
    ax.set_title('Cost on the test data')
    plt.show()

def plot_training_accuracy(training_accuracy, num_epochs, 
                           training_accuracy_xmin, training_set_size):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.arange(training_accuracy_xmin, num_epochs), 
            [accuracy*100.0/training_set_size 
             for accuracy in training_accuracy[training_accuracy_xmin:num_epochs]],
            color='#2A6EA6')
    ax.set_xlim([training_accuracy_xmin, num_epochs])
    ax.grid(True)
    ax.set_xlabel('Epoch')
    ax.set_title('Accuracy (%) on the training data')
    plt.show()

def plot_overlay(test_accuracy, training_accuracy, num_epochs, xmin,
                 training_set_size):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.arange(xmin, num_epochs), 
            [accuracy/100.0 for accuracy in test_accuracy], 
            color='#2A6EA6',
            label="Accuracy on the test data")
    ax.plot(np.arange(xmin, num_epochs), 
            [accuracy*100.0/training_set_size 
             for accuracy in training_accuracy], 
            color='#FFA933',
            label="Accuracy on the training data")
    ax.grid(True)
    ax.set_xlim([xmin, num_epochs])
    ax.set_xlabel('Epoch')
    ax.set_ylim([90, 100])
    plt.legend(loc="lower right")
    plt.show()

if __name__ == "__main__":
    filename = raw_input("Enter a file name: ")
    num_epochs = int(raw_input(
        "Enter the number of epochs to run for: "))
    training_cost_xmin = int(raw_input(
        "training_cost_xmin (suggest 200): "))
    test_accuracy_xmin = int(raw_input(
        "test_accuracy_xmin (suggest 200): "))
    test_cost_xmin = int(raw_input(
        "test_cost_xmin (suggest 0): "))
    training_accuracy_xmin = int(raw_input(
        "training_accuracy_xmin (suggest 0): "))
    training_set_size = int(raw_input(
        "Training set size (suggest 1000): "))
    lmbda = float(raw_input(
        "Enter the regularization parameter, lambda (suggest: 5.0): "))
    main(filename, num_epochs, training_cost_xmin, 
         test_accuracy_xmin, test_cost_xmin, training_accuracy_xmin,
         training_set_size, lmbda)
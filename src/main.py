import numpy as np
import matplotlib.pyplot as plt
def test_setup():
    print("Environnement de simulation prêt !")
    #création d'une simple sinusoïde pour tester le graphique
    t = np.linspace(0,10,100)
    y = np.sin(t)
    plt.plot(t,y)
    plt.title("Test d'environnement - Système de Trajectoire")
    plt.show()
    if __name__ == "__main__":
        test_setup()


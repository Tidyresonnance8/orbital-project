import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from physics import MU_EARTH, R_EARTH
from solver import orbit_equations
#import os

def run_simulation():
    print("Initialisation de la mission orbitale...")
    # Conditions Initiales (Altitude 400km)
    altitude = 400000
    r0 = R_EARTH + altitude
    v0 = np.sqrt(MU_EARTH / r0) * 1.1 # Vitesse orbitale pour une orbite circulaire et j'augmente la vitesse de 10%
    # Vecteur d'état initial [x, y, z, vx, vy, vz]
    initial_state = [r0, 0, 0, 0, v0, 0]

    # Temps de simulation (environ 90 min pour une orbite LEO)
    t_span = (0, 5600)
    t_eval = np.linspace(t_span[0], t_span[1], 1000) # Points où on veut calculer la position

    # Résolution avec RK45 (variante de Runge-Kutta du cours)
    sol = solve_ivp(
        orbit_equations,
        t_span,
        initial_state,
        args=(MU_EARTH,),
        t_eval=t_eval,
        method='RK45', # Méthode de Runge-kutta d'ordre 4(5)
        rtol=1e-9      # Tolérance relative (très précis comme dans ton cours)
    )
    
    # Affichage
    plt.figure(figsize=(8, 8))
    plt.plot(sol.y[0], sol.y[1], label="Trajectoire Satellite")

    # Dessin de la Terre
    theta = np.linspace(0, 2*np.pi, 100)
    x_earth = R_EARTH * np.cos(theta)
    y_earth = R_EARTH * np.sin(theta)
    plt.fill(x_earth, y_earth, 'b', alpha=0.2, label="Terre")
  

    plt.axis('equal')
    plt.grid(True, linestyle='--')
    plt.title("Simulation de trajectoire orbitale - Méthode RK45")
    plt.xlabel("Position X (m)")
    plt.ylabel("Position Y (m)")
    plt.legend()

    print("Simulation terminée. Affichage du graphique...")
    
    import os
    if not os.path.exists('results'):
        os.makedirs('results')
    
    plt.savefig('results/circular_orbit.png', dpi=300) #dpi=300 pour une qualité "pro"
    print("Graphique sauvegardé dans results/circular_orbit.png")
    
    plt.show()
if __name__ == "__main__":
    run_simulation()


import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from physics import MU_EARTH, R_EARTH, J2, DIST_MOON, OMEGA_MOON
from solver import orbit_equations_3body 
import os
from mpl_toolkits.mplot3d import Axes3D
from solver import get_orbital_elements
from my_solver import my_rk4_solver
from matplotlib.animation import FuncAnimation


def run_simulation():
    # Configuration 
    print("Initialisation de la mission orbitale...")
    if not os.path.exists('results'):
        os.makedirs('results')

    # Conditions Initiales (Altitude 400km)
    v_ratio = 1.1
    altitude = 400000
    r0 = R_EARTH + altitude
    # Je définis l'inclinaison
    inc = np.radians(45)
    v0 = np.sqrt(MU_EARTH / r0) * 1.1 # Vitesse orbitale pour une orbite circulaire et j'augmente la vitesse de 10%
    vy0 = v0 * np.cos(inc)
    vz0 = v0 * np.sin(inc)
    # Vecteur d'état initial [x, y, z, vx, vy, vz]
    initial_state = [r0, 0, 0, 0, vy0, vz0]

    # Temps de simulation (environ 90 min pour une orbite LEO)
    t_span = (0, 100000)
    #t_eval = np.linspace(t_span[0], t_span[1], 2000) # Points où on veut calculer la position
    
    # Résolution avec RK45 (variante de Runge-Kutta du cours)
    #sol = solve_ivp(
    #  orbit_equations,
    #    t_span,
    #    initial_state,
    #    args=(MU_EARTH,),
    #    t_eval=t_eval,
    #    method='RK45', # Méthode de Runge-kutta d'ordre 4(5)
    #    rtol=1e-9      # Tolérance relative (très précis comme dans ton cours)
    #)

    # On définit un pas de temps fixe (ex: 10 secondes)
    h = 60.0  # pas de temps fixe

    # Utilisation de mon solver à la place de Scipy
    t_rk4, y_rk4 = my_rk4_solver(
        orbit_equations_3body,
        t_span,
        initial_state,
        h=h,
        args=(MU_EARTH,)
    )

    # on simule l'objet 'sol' de scipy
    class SimpleSol:
        def __init__(self,t,y):
            self.t = t
            self.y = y
    
    sol = SimpleSol(t_rk4, y_rk4)

    # Analyse SCientifique
    x, y, z = sol.y[0], sol.y[1], sol.y[2]
    vx, vy, vz = sol.y[3], sol.y[4], sol.y[5]

    # Calcul des distances et des vitesses
    r = np.sqrt(x**2 + y**2 + z**2)
    v_mag = np.sqrt(vx**2 + vy**2 + vz**2)

    # Energie specifique : E = Ec + Ep
    # Formule : 0.5*v^2 - mu/r
    total_energy = (0.5 * v_mag**2) - (MU_EARTH / r)

    # Dérive relative de l'énergie (Erreur numérque)
    energy_drift = (total_energy - total_energy[0]) / total_energy[0]
    
    # Extraction de Omega au cours du temps
    omegas = np.array([get_orbital_elements(sol.y[:, i]) for i in range(len(sol.t))])

    # Calcul de la vitesse de précession numérique (pente de la courbe)
    # On va utiliser la regression linéaire simple pour trouver la pente
    slope_num, intercept = np.polyfit(sol.t, np.unwrap(omegas), 1)

    # Calcul théorique 
    p = r0 * (v_ratio**2)
    a = r0 / (2 - v_ratio**2)  # Demi-grand axe initial
    n = np.sqrt(MU_EARTH / a**3)
    i = np.radians(45)
    
    # Formule de précession nodle J2 (analytique)
    omega_dot_th = -(1.5) * J2 * (R_EARTH / p)**2 *n * np.cos(i)

    # Calcul de l'erreur
    error_pct = abs((slope_num - omega_dot_th) / omega_dot_th) * 100

    print(f"\n--- ANALYSE J2 (h={h}s) ---")
    #print(f"Précession Numérique : {slope_num:.4e} rad/s")
    #print(f"Précession Théorique : {omega_dot_th:.4e} rad/s")
    print(f"Erreur Relative : {error_pct:.6f} %")

    # Affichage
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Trajectoire du satellite
    #ax.plot(sol.y[0], sol.y[1], sol.y[2], 'r-', label="Trajectoire avec $J_2$")

    # Dessin de la Terre
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
    x_earth = R_EARTH * np.cos(u) * np.sin(v)
    y_earth = R_EARTH * np.sin(u) * np.sin(v)
    z_earth = R_EARTH * np.cos(v)
    ax.plot_wireframe(x_earth, y_earth, z_earth, color='b', alpha=0.1)
    
    # Objets pour l'animation
    line, = ax.plot([], [], [], 'r-', alpha=0.5, label="Trajectoire")
    point, = ax.plot([], [], [], 'ro', markersize=6, label="Satellite")
    moon_point, = ax.plot([], [], [], 'ko', markersize=10, label="Lune")

    # Limites des axes
    zoom_on_moon = True # Change à False pour revenir au satellite
    if zoom_on_moon:
        limit = DIST_MOON * 1.2
    else:
        limit = np.max(np.abs(sol.y[0:3, :])) * 1.2
    #max_range = np.max(np.abs(sol.y[0:3, :]))
    ax.set_xlim(-limit, limit) # après je remplacerai par max_range pour avoir la configuration initiale
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)
    ax.set_title(f"Animation Orbitale J2 - Pas h={h}s")
    ax.legend()

    moon_point, = ax.plot([], [], [], 'ko', markersize=8, label="Lune")

    # Logique De L'Animation
    def update_plot(num, data, line, point):
        # Mise à jour de la traînée (ligne) et du satellite (point)
        point.set_data(data[0:2, num-1:num])
        point.set_3d_properties(data[2, num-1:num])
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])
        
        # Position de la lune à l'instant t
        t_curr = sol.t[num-1]
        x_l = DIST_MOON * np.cos(OMEGA_MOON * t_curr)
        y_l = DIST_MOON * np.sin(OMEGA_MOON * t_curr)
        moon_point.set_data([x_l], [y_l])
        moon_point.set_3d_properties([0])  # Grâce à ça la Lune se trouve dans le plan z
        
        return line, point, moon_point


    # Lancement de l'animation
    ani = FuncAnimation(fig, update_plot, frames=len(sol.t),
                        fargs=(sol.y, line, point), interval=20, blit=False)
 
    plt.show()
    

if __name__ == "__main__":
    run_simulation()



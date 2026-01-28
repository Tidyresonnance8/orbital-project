import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from physics import MU_EARTH, R_EARTH, J2
from solver import orbit_equations
import os
from mpl_toolkits.mplot3d import Axes3D
from solver import get_orbital_elements


def run_simulation():
    # Configuration 
    print("Initialisation de la mission orbitale...")
    if not os.path.exists('results'):
        os.makedirs('results')

    # Conditions Initiales (Altitude 400km)
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
    t_span = (0, 30000)
    t_eval = np.linspace(t_span[0], t_span[1], 2000) # Points où on veut calculer la position
    
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
    v_ratio = 1.1
    p = r0 * (v_ratio**2)
    a = r0 / (2 - v_ratio**2)  # Demi-grand axe initial
    n = np.sqrt(MU_EARTH / a**3)
    i = np.radians(45)
    
    # Formule de précession nodle J2 (analytique)
    omega_dot_th = -(1.5) * J2 * (R_EARTH / p)**2 *n * np.cos(i)

    # Calcul de l'erreur
    error_pct = abs((slope_num - omega_dot_th) / omega_dot_th) * 100

    print(f"\n--- ANALYSE J2 ---")
    print(f"Précession Numérique : {slope_num:.4e} rad/s")
    print(f"Précession Théorique : {omega_dot_th:.4e} rad/s")
    print(f"Erreur Relative : {error_pct:.6f} %")

    # Affichage
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Trajectoire du satellite
    ax.plot(sol.y[0], sol.y[1], sol.y[2], 'r-', label="Trajectoire avec $J_2$")

    # Dessin de la Terre
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
    x_earth = R_EARTH * np.cos(u) * np.sin(v)
    y_earth = R_EARTH * np.sin(u) * np.sin(v)
    z_earth = R_EARTH * np.cos(v)
    ax.plot_wireframe(x_earth, y_earth, z_earth, color='b', alpha=0.1)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title("Simulation Orbitale 3D avec Perturbation $J_2$")
    ax.legend()

    max_range = np.array([sol.y[0].max()-sol.y[0].min(),
                          sol.y[1].max()-sol.y[1].min(),
                          sol.y[2].max()-sol.y[2].min()]).max() / 2.0
    
    mid_x = (sol.y[0].max()+sol.y[0].min()) * 0.5
    mid_y = (sol.y[1].max()+sol.y[1].min()) * 0.5
    mid_z = (sol.y[2].max()+sol.y[2].min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.savefig('results/orbit_3d.png')
    plt.show()

if __name__ == "__main__":
    run_simulation()



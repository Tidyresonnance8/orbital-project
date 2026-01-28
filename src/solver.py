import numpy as np
from physics import J2, R_EARTH

def orbit_equations(t, state, mu):
    """
    Définit les équations différentielles du mouvement (Problème à 2 corps).
    state = [x, y, z, vx, vy, vz]
    """
    x, y, z, vx, vy, vz = state
    r = np.sqrt(x**2 + y**2 + z**2)

    # Accélération selon la loi de Newton 
    ax = -mu * x / r**3
    ay = -mu * y / r**3
    az = -mu * z / r**3

    # Accélération due à la perturbation J2
    factor = (3/2) * J2 * mu * (R_EARTH**2) / (r**5)

    z_over_r_sq = (z/r)**2

    ax_j2 = factor * x * (5 * z_over_r_sq - 1)
    ay_j2 = factor * y * (5 * z_over_r_sq - 1)
    az_j2 = factor * z * (5 * z_over_r_sq - 3)

    # Accélération des sommes Newtonienne et Perturbations J2
    return [vx, vy, vz, ax + ax_j2, ay + ay_j2, az + az_j2]

def get_orbital_elements(state):
    """
    Analyse géométrique pour extraire la longitude du noeud ascendant (Omega).
    C'est essentiel pour mesurer la précession nodale J2.
    """
    x, y, z, vx, vy, vz = state

    # Vecteur position et vitesse
    r_vec = np.array([x, y, z])
    v_vec = np.array([vx, vy, vz])

    # Vecteur moment cinétique spécifique (h = r*v)
    h_vec = np.cross(r_vec,v_vec)

    # Vecteur ligne des noeuds (n = k*h, où k est l'axe z [0,0,1])
    # n pointe vers le noeud ascendant (là où l'orbite coupe l'équateur vers le nord)
    n_vec = np.array([-h_vec[1], h_vec[0], 0])
    n_mag = np.linalg.norm(n_vec)

    if n_mag == 0:
        return 0 # Orbite équatoriale (pas de noeud)
    
    # Calcul de Omega (Angle entre l'axe X et le vecteur ligne des noeuds)
    Omega = np.arccos(n_vec[0] / n_mag)
    if n_vec[1] < 0:
        Omega = 2 * np.pi - Omega
    return Omega
import numpy as np

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

    return [vx, vy, vz, ax, ay, az]
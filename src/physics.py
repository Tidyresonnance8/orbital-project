G = 6.67430e-11        # constante gravitationnelle (m^3 kg^-1 s^2)
M_EARTH = 5.972e24     # Masse de la Terre (kg)
MU_EARTH = G * M_EARTH # Paramètre gravitationnel standard (mu)
R_EARTH = 6371000.0    # Rayon moyen de la terre
J2 = 1.08262668e-3     # Coefficient de perturbation J2

# Constantes Lunaires
MU_MOON = 4.9048695e12  # m^3/s^2
DIST_MOON = 384400000.0 # Distance Terre-Lune moyenne en m
OMEGA_MOON = 2.6617e-6  # Vitesse angulaire de la lune (rad/s)

# Données : [Masse (kg), Distance au soleil (m), Vitesse orbitale (m/s)]
SOLAR_SYSTEM_DATA = {
    "Sun": [1.989e30, 0, 0],
    "Mercury": [3.301e23, 5.791e10, 47360],
    "Venus": [4.867e24, 1.082e11, 35020],
    "Earth": [5.972e24, 1.496e11, 29780],
    "Mars": [6.390e23, 2.279e11, 24070],
    "Jupiter": [1.898e27, 7.785e11, 13070],
    "Saturn": [5.683e26, 1.433e12, 9690],
    "Uranus": [8.681e25, 2.871e12, 6810],
    "Neptune": [1.024e26, 4.495e12, 5430],
}

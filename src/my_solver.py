import numpy as np

def rk4_step(f, t, y, h, args=()):
    """
    Calcule une étape d'intégration RK4 classique.
    
    :param f: la fonction dérivée (orbit_equations)
    :param t: temps actuel
    :param y: vecteur d'état actuel
    :param h: pas de temps
    """
    k1 = np.array(f(t, y, *args))
    k2 = np.array(f(t + h/2, y + h/2 * k1, *args))
    k3 = np.array(f(t + h/2, y + h/2 * k2, *args))
    k4 = np.array(f(t + h, y + h * k3, *args))

    return y + (h/6.0) * (k1 + 2*k2 + 2*k3 + k4)

def my_rk4_solver(f, t_span, y0, h, args=()):
    """
    Simulation la trajectoire complète en itérant rk4_step

    """
    t0, tf = t_span
    t_values = np.arange(t0, tf, h)
    y_values = np.zeros((len(t_values), len(y0)))

    y_values[0] = y0

    for i in range(len(t_values)-1):
        y_values[i+1] = rk4_step(f, t_values[i], y_values[i], h, args)
    return t_values, y_values.T

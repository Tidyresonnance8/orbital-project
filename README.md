# Orbital Trajectory System
## Overview
This project is developed as a personal research initiative by an Engineering Student at **UCLouvain** (Applied Mathematics & Computer Science). The goal is to simulate and visualize orbital trajectories using Newtonian mechanics and numerical integration methods.

## Objectives
* **Physics:** Implement the 2-body problem and model orbital mechaics.
* **Mathematics:** Solve the **Cauchy Problem** ($y'(t) = f(t, y(t))$) using Runge-Kutta 4th Order (RK45) method.
* **Software:** Build a modular python architecture (Physics / Solver / Main).

## Simulation & Stability Analysis

### 1. Elliptical Orbit (Keplerian Motion)
By increasing the initial orbital velocty by 10%, we transition from a circular to an elliptical orbit. This demonstrates the conservation of angular momentum and the first law of kepler.

![Trajectory](results/orbit_trajectory.png)

### 2. Numerical Stability (Energy conservation)
A key challenge in numerical integration is the accumulation of truncation errors. Following the **Numerical Methods** curriculum, I validated the solver by monitoring the specific mechanincal energy: $$E = \frac{1}{2}v^2 - \frac{\mu}{r}$$

![Energy Drift](results/energy_conservation.png)

*Observation: The relative energy drift $\Delta E / E_0$ remains below $10^{-10}$,confirming the high precision and stability of the RK45 adaptive step-size integrator.*

## Tech Stack
* **Language:** Python 3.12
* **Libraries:** Numpy, Scipy, Matplotlib
* **Environment:** Linux Ubuntu

I implemented a 4th-order Runge-Kutta integrator based on the Numerical Methods curriculum at UCLouvain to ensure energy conservation and trajectory stability in a 2-body simulation.


## Simulation Results
Here is the output of the circular orbit simulation (Altitude: 400km) using the RK45 integrator:
![Circular Orbit](results/circular_orbit.png)

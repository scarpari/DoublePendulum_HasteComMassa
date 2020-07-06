import math
import numpy as np

class dp_physics:

    def __init__(self, g, m1, m2, t1, t2, w1, w2, L1, L2):
        self.g = g
        self.m1 = m1
        self.m2 = m2
        self.t1 = t1  # teta
        self.t2 = t2
        self.L1 = L1  # comprimento da haste
        self.L2 = L2
        self.w1 = w1  # omega
        self.w2 = w2

    def potential_energy(self):
        '''Verificado'''
        g = self.g
        m1 = self.m1
        m2 = self.m2
        t1 = self.t1
        t2 = self.t2
        L1 = self.L1
        L2 = self.L2

        h1 = -L1*math.cos(t1) # Parametrizando o teto X0 como referencia
        h2 = h1 - L2*math.cos(t2)
        return m1*g*h1 + m2*g*h2

    def kinetic_energy_A(self):
        m1 = self.m1
        w1 = self.w1
        L1 = self.L1

        return 0.5*m1*(w1*L1)**2

    def kinetic_energy_B(self):
        m2 = self.m2
        t1 = self.t1
        t2 = self.t2
        L1 = self.L1
        L2 = self.L2
        w1 = self.w1
        w2 = self.w2

        K2 = 0.5*m2*((L1*w1)**2 + (L2*w2)**2 + 2*L1*L2*w1*w2*math.cos(t1 - t2))
        return K2

    def kinetic_energy(self):
        return self.kinetic_energy_A() + self.kinetic_energy_B()

    def mec_energy(self):
        return self.kinetic_energy() + self.potential_energy()

    def double_pendulum_physics(self, t1, t2, w1, w2):
        m1 = self.m1
        L1 = self.L1
        m2 = self.m2
        L2 = self.L2
        g = self.g

        aux1 = (L2/L1)*(m2/(m1 + m2))*math.cos(t1 - t2)
        aux2 = (L1/L2)*math.cos(t1 - t2)
        aux3 = -(L2/L1)*(m2/(m1 + m2))*(w2**2)*math.sin(t1 - t2) - \
            (g/L1)*math.sin(t1)
        aux4 = (L1/L2)*(w1**2)*math.sin(t1 - t2) - (g/L2)*math.sin(t2)

        total_1 = (aux3 - aux1*aux4)/(1 - aux1*aux2)
        total_2 = (aux4 - aux2*aux3)/(1 - aux1*aux2)

        return np.array([w1, w2, total_1, total_2])

    def time_step(self, dt):
        # Peguei do github
        """
                Advances one time step using RK4 (classical Runge-Kutta method).
                                                                                    """
        t1 = self.t1
        w1 = self.w1
        t2 = self.t2
        w2 = self.w2

        y = np.array([t1, t2, w1, w2])  #array de coordenadas tetas e omegas

        # compute the RK4 constants
        k1 = self.double_pendulum_physics(*y)
        k2 = self.double_pendulum_physics(*(y + dt * k1 / 2))
        k3 = self.double_pendulum_physics(*(y + dt * k2 / 2))
        k4 = self.double_pendulum_physics(*(y + dt * k3))

        # compute the RK4 right-hand side
        R = 1.0 / 6.0 * dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        # update the angles and angular velocities
        self.t1 += R[0]
        self.t2 += R[1]
        self.w1 += R[2]
        self.w2 += R[3]
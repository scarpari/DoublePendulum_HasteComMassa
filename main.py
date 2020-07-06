""" Programa de simulacao de um Pendulo Duplo para o trabalho de FIS-32 """
import window_draw
import pygame
import sys
import math

f = open("data.txt", "w")
f.write("===================================================================="
        " SIMULACAO DO PENDULO DUPLO "
        "===================================================================="
        "\n\n"
        "Dados fixos utilizados na simulacao: ")

def main(m1, m2, L1, L2, t1, t2):
    g = 9.81
    dt = 0.041
    dados_fixos = "\n   g = %f m/s^2\n   m1 = %f kg\n   m2 = %f kg\n   t1 = %f rad\n" \
                  "   t2 = %f rad\n   w1 = %f rad/s\n   w2 = %f rad/s\n   " \
                  "L1 = %f m\n   L2 = %f m\n\n\n"
    f.write(dados_fixos % (g, m1, m2, t1, t2, w1, w2, L1, L2))
    # default window dimensions
    width = height = 500

    # initialize the double pendulum
    from physics import dp_physics
    system = dp_physics(g, m1, m2, t1, t2, w1, w2, L1, L2)

    # E0 = initial mechanical energy of the system
    E0 = system.mec_energy()

    # maximum energy change (compared to E0): too large => unstable simulation
    max_dE = 0
    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Pêndulo Duplo _ FIS-32")

    step = 0
    while True:
        window_draw.draw(system, window, width, height, dt)
        clock.tick(25)  # limita o while a 25 por segundo para nao crashar
        system.time_step(dt)
        Et = system.mec_energy()
        K1 = system.kinetic_energy_A()
        K2 = system.kinetic_energy_B()
        Kt = system.kinetic_energy()
        max_dE = max(abs(Et - E0), max_dE)
        line = "[%u] t = %f s   Et = %f J   E0 = %f J  K1 = %f J  K2 = %f J  Kt = %f J  |Et - E0| = %f J  " + \
                "|Et - E0|_max = %f J\n"
        sys.stdout.write(line % (step, step * dt, Et, E0, K1, K2, Kt, abs(Et - E0), max_dE))
        f.write(line % (step, step * dt, Et, E0, K1, K2, Kt, abs(Et - E0), max_dE))
        step += 1

        # Checando os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.VIDEORESIZE:
                (width, height) = event.size
                window = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[273]:
            dt *= 1.05
        if pressed_keys[274]:
            dt /= 1.05

if __name__ == "__main__":
    sys.stdout.write("\nPendulo Duplo\n\n")
    ans = input("Deseja forncer os valores do processo? (S ou N) - Caso nao queira iremos gera-los para voce.  ")
    if ans =="S" or ans == "s":
        m1 = float(input("Digite o Valor da massa 1 (kg): "))
        m2 = float(input("Digite o Valor da massa 2 (kg): "))
        L1 = float(input("Digite o Valor do comprimento da haste 1 (m): "))
        L2 = float(input("Digite o Valor do comprimento da haste 2 (m): "))
        t1 = float(input("Digite o Valor de teta 1 (°): "))
        t2 = float(input("Digite o Valor de teta 2 (°): "))
        w1 = float(input("Digite o Valor de omega 1 (rad/s): "))
        w2 = float(input("Digite o Valor de omega 2 (rad/s): "))
    else:
        m1 = 5
        m2 = 6
        t1 = 180
        t2 = 45
        w1 = 0
        w2 = 0
        L1 = 1
        L2 = 1
    t2 = math.pi * t2 / 180
    t1 = math.pi * t1 / 180
    main(m1, m2, L1, L2, t1, t2)
    sys.stdout.write("\n\nProjeto de simulação desenvolvido por Ricardo P. Scarpari\n")
    f.close()
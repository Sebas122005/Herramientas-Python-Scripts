import random
import math

# --------------------------
# Parámetros ajustables
# --------------------------
capital_inicial = 30
inversion_inicial = 2
ganancia_margen = 0.8         # margen de ganancia sobre la apuesta
max_martingala = 2            # número máximo de martingalas
sesiones = 7                  # cantidad de días
ops_por_sesion = 10           # cantidad de señales por sesión
target_signal_win_rate = 0.85 # winrate esperado por señal (histórico observado)
# --------------------------

# Calcular probabilidad por intento para lograr el target_signal_win_rate
p_intento = 1 - (1 - target_signal_win_rate) ** (1 / (max_martingala + 1))
print(f"Probabilidad por intento ajustada: {p_intento:.3f} (para target de {target_signal_win_rate*100:.1f}% por señal)\n")

def simular_senal(capital, inversion, p_intento):
    """Simula una señal completa con martingala"""
    intentos = 0
    apuesta = inversion
    total_losses = 0
    global wins_intentos, losses_intentos

    while intentos <= max_martingala:
        intentos += 1
        if random.random() <= p_intento:
            ganancia = apuesta * ganancia_margen
            capital += ganancia
            wins_intentos += 1
            return capital, ganancia, total_losses, True, intentos
        else:
            capital -= apuesta
            total_losses += apuesta
            losses_intentos += 1
            apuesta *= 2

    # si llegó aquí = señal perdida
    return capital, 0, total_losses, False, intentos

# --------------------------
# Simulación completa
# --------------------------
capital = capital_inicial
wins_signals = losses_signals = 0
wins_intentos = losses_intentos = 0

print(f"--- INICIO DE SIMULACIÓN ({sesiones} sesiones x {ops_por_sesion} señales/día) ---")
print(f"Capital inicial: ${capital:.2f}\n")

for d in range(1, sesiones + 1):
    start_capital = capital
    session_gains = session_losses = 0
    wins_s = losses_s = 0
    intentos_sesion = 0

    for _ in range(ops_por_sesion):
        capital, gain, loss, win, intentos = simular_senal(capital, inversion_inicial, p_intento)
        session_gains += gain
        session_losses += loss
        intentos_sesion += intentos
        if win:
            wins_s += 1
        else:
            losses_s += 1

    wins_signals += wins_s
    losses_signals += losses_s

    print(f"Sesión {d}:")
    print(f"  Start capital: ${start_capital:.2f}")
    print(f"  Gains: ${session_gains:.2f}")
    print(f"  Losses: ${session_losses:.2f}")
    print(f"  Net: ${(session_gains - session_losses):.2f}")
    print(f"  End capital: ${capital:.2f}")
    print(f"  Señales ganadas: {wins_s}/{ops_por_sesion} | perdidas: {losses_s}/{ops_por_sesion}")
    print(f"  Intentos/apuestas en la sesión: {intentos_sesion}")
    print(f"  -> Acumulado hasta día {d}: wins_signals = {wins_signals}, loss_signals = {losses_signals}, wins_intentos = {wins_intentos}, losses_intentos = {losses_intentos}\n")

# --------------------------
# Estadísticas finales
# --------------------------
total_signals = wins_signals + losses_signals
total_intentos = wins_intentos + losses_intentos

print("--- ESTADÍSTICA FINAL ---")
print(f"Capital final: ${capital:.2f}")
print(f"Profit total: ${capital - capital_inicial:.2f}")
print(f"Señales iniciadas: {total_signals}")
print(f"Intentos totales realizados: {total_intentos}")
print(f"Señales ganadoras: {wins_signals} | perdidas: {losses_signals}")
print(f"Tasa por señal: {wins_signals / total_signals * 100:.2f}%")
print(f"Tasa por intento: {wins_intentos / total_intentos * 100:.2f}%")

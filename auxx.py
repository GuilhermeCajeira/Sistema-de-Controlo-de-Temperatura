class PIDController:
    def __init__(self, setpoint, kp, ki, kd):
        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, current_value):
        error = self.setpoint - current_value

        # Termo Proporcional
        P = self.kp * error

        # Termo Integral
        self.integral += error
        I = self.ki * self.integral

        # Termo Derivativo
        D = self.kd * (error - self.prev_error)

        # Soma dos termos
        output = P + I + D

        # Atualiza o erro anterior
        self.prev_error = error

        return output

# Simulação do Sistema de Controle de Temperatura
class TemperatureSystem:
    def __init__(self):
        self.current_temperature = 20.0

    def update_temperature(self, heat_power):
        # Modelo simples para simular a mudança de temperatura
        delta_time = 1.0  # intervalo de tempo
        thermal_constant = 0.1  # constante térmica do sistema
        target_temperature = 25.0  # temperatura desejada

        error = target_temperature - self.current_temperature
        temperature_change = heat_power * delta_time / thermal_constant + 0.1 * error
        self.current_temperature += temperature_change

        return self.current_temperature

# Simulação de Controle com PID
def simulate_pid_control(pid, system):
    time_steps = 100
    temperatures = []

    for _ in range(time_steps):
        current_temperature = system.current_temperature
        control_signal = pid.compute(current_temperature)
        updated_temperature = system.update_temperature(control_signal)

        temperatures.append(updated_temperature)

    return temperatures

# Parâmetros do PID
setpoint_temperature = 25.0
kp = 1.0
ki = 0.1
kd = 0.01

# Inicialização do PID
pid_controller = PIDController(setpoint_temperature, kp, ki, kd)

# Inicialização do Sistema de Temperatura
temperature_system = TemperatureSystem()

# Simulação do Controle PID
simulated_temperatures = simulate_pid_control(pid_controller, temperature_system)

# Plotagem dos Resultados (requer matplotlib)
import matplotlib.pyplot as plt

plt.plot(simulated_temperatures, label='Temperatura Simulada')
plt.axhline(setpoint_temperature, color='r', linestyle='--', label='Temperatura Desejada')
plt.title('Simulação de Controle PID de Temperatura')
plt.xlabel('Tempo')
plt.ylabel('Temperatura')
plt.legend()
plt.show()

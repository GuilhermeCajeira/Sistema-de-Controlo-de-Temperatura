import random
import time

class TemperatureSensor:
    def __init__(self):
        self.current_temperature = 20.0  # Temperatura inicial

    def read_temperature(self):
        # Simula a leitura do sensor
        variation = random.uniform(-1.0, 1.0)
        self.current_temperature += variation
        return self.current_temperature

class PIDController:
    def __init__(self, desired_temperature):
        self.desired_temperature = desired_temperature  # Temperatura desejada
        self.target_temperature_range = 1.0  # Faixa de temperatura permitida

        # Valores de PID configurados no código
        self.kp = 1.0  # Ganho proporcional
        self.ki = 0.1  # Ganho integral
        self.kd = 0.01  # Ganho derivativo

        self.prev_error = 0.0
        self.integral = 0.0

        self.output_limit = 5.0  # Limita a mudança máxima de saída

    def adjust_temperature(self, current_temperature):
        error = self.desired_temperature - current_temperature

        # Termo proporcional
        proportional = self.kp * error

        # Termo integral
        self.integral += self.ki * error

        # Termo derivativo
        derivative = self.kd * (error - self.prev_error)

        # Saída PID
        output = proportional + self.integral + derivative

        # Limita a mudança de saída para evitar mudanças súbitas
        output = max(-self.output_limit, min(output, self.output_limit))

        # Atualiza o erro anterior para a próxima iteração
        self.prev_error = error

        # Aplica a saída do controle
        self.apply_output(output)

    def apply_output(self, output):
        # Implementa a ação a ser tomada com base na saída do PID
        if output > 0:
            print(f"Heater activated with power: {output:.2f}")
        elif output < 0:
            print(f"Air conditioner activated with power: {-output:.2f}")
        else:
            print("Heater and Air conditioner deactivated")

def print_menu():
    print("\n=== Temperature Control System ===")
    print("1. Choose temperature")
    print("0. Exit")

def choose_temperature(controller):
    temperature = float(input("Enter desired temperature: "))
    controller.desired_temperature = temperature
    print(f"Desired temperature set to {temperature}°C")

if __name__ == "__main__":
    initial_desired_temperature = float(input("Enter initial desired temperature: "))
    temperature_sensor = TemperatureSensor()
    pid_controller = PIDController(initial_desired_temperature)

    try:
        while True:
            print_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                choose_temperature(pid_controller)
            elif choice == "0":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

            while True:
                current_temperature = temperature_sensor.read_temperature()
                print(f"Current temperature: {current_temperature:.2f}°C")

                pid_controller.adjust_temperature(current_temperature)

                time.sleep(1)  # Intervalo de leitura do sensor

    except KeyboardInterrupt:
        print("Program interrupted by the user")

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

class TemperatureController:
    def __init__(self, desired_temperature):
        self.desired_temperature = desired_temperature  # Temperatura desejada
        self.target_temperature_range = 1.0  # Faixa de temperatura permitida
        self.air_conditioner_active = False
        self.heater_active = False

    def adjust_temperature(self, current_temperature):
        temperature_difference = current_temperature - self.desired_temperature

        if abs(temperature_difference) > self.target_temperature_range:
            if temperature_difference > 0:
                self.activate_air_conditioner()
                self.deactivate_heater()
            else:
                self.activate_heater()
                self.deactivate_air_conditioner()
        else:
            self.deactivate_air_conditioner()
            self.deactivate_heater()

    def activate_air_conditioner(self):
        if not self.air_conditioner_active:
            print("Air conditioner activated")
            self.air_conditioner_active = True

    def deactivate_air_conditioner(self):
        if self.air_conditioner_active:
            print("Air conditioner deactivated")
            self.air_conditioner_active = False

    def activate_heater(self):
        if not self.heater_active:
            print("Heater activated")
            self.heater_active = True

    def deactivate_heater(self):
        if self.heater_active:
            print("Heater deactivated")
            self.heater_active = False

def print_menu():
    print("\n=== Temperature Control System ===")
    print("1. Choose temperature")
    print("0. Exit")

def choose_temperature(controller):
    temperature = float(input("Enter desired temperature: "))
    controller.desired_temperature = temperature
    print(f"Desired temperature set to {temperature}°C")

if __name__ == "__main__":
    temperature_sensor = TemperatureSensor()
    desired_temperature = float(input("Enter initial desired temperature: "))
    hvac_controller = TemperatureController(desired_temperature)

    try:
        while True:
            print_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                choose_temperature(hvac_controller)
            elif choice == "0":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

            while True:
                current_temperature = temperature_sensor.read_temperature()
                print(f"Current temperature: {current_temperature:.2f}°C")

                hvac_controller.adjust_temperature(current_temperature)

                time.sleep(1)  # Intervalo de leitura do sensor

    except KeyboardInterrupt:
        print("Program interrupted by the user")

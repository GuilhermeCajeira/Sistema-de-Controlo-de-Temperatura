import random
import time
import tkinter as tk
from tkinter import messagebox

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

    def auto_regulate_temperature(self):
        self.heating = False
        self.cooling = False

    def heat_room(self):
        self.heating = True
        self.cooling = False

    def cool_room(self):
        self.heating = False
        self.cooling = True


class TemperatureControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Control System")

        self.temperature_sensor = TemperatureSensor()
        self.desired_temperature = tk.DoubleVar(value=25.0)
        self.temp_controller = TemperatureController(self.desired_temperature.get())

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Desired Temperature:").pack()
        entry_temperature = tk.Entry(self.root, textvariable=self.desired_temperature)
        entry_temperature.pack(pady=5)

        tk.Button(self.root, text="Choose Temperature", command=self.choose_temperature).pack(pady=5)
        tk.Button(self.root, text="Automatically Regulate", command=self.temp_controller.auto_regulate_temperature).pack(pady=5)
        tk.Button(self.root, text="Heat Room", command=self.temp_controller.heat_room).pack(pady=5)
        tk.Button(self.root, text="Cool Room", command=self.temp_controller.cool_room).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.destroy).pack(pady=5)

        # Atualizações de temperatura
        self.label_temperature = tk.Label(self.root, text="Current Temperature: 20.0°C")
        self.label_temperature.pack(pady=10)
        self.root.after(1000, self.update_temperature_display)

    def choose_temperature(self):
        self.temp_controller.desired_temperature = self.desired_temperature.get()
        messagebox.showinfo("Temperature Control System", f"Desired temperature set to {self.desired_temperature.get()}°C")

    def update_temperature_display(self):
        current_temperature = self.temperature_sensor.read_temperature()
        self.label_temperature.config(text=f"Current Temperature: {current_temperature:.2f}°C")
        self.temp_controller.adjust_temperature(current_temperature)
        self.root.after(1000, self.update_temperature_display)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")
    root.configure(bg='light blue')
    app = TemperatureControlApp(root)
    root.mainloop()

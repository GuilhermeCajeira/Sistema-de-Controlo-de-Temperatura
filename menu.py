import tkinter as tk
from tkinter import messagebox
import random

class TemperatureControlSystem:
    def __init__(self):
        self.sensor_temperature = 25.0
        self.target_temperature = 25.0
        self.heating = False
        self.cooling = False

    def measure_temperature(self):
        # Simulação da leitura do sensor de temperatura
        variation = random.uniform(-1.0, 1.0)
        self.sensor_temperature += variation
        return round(self.sensor_temperature, 2)

    def regulate_temperature(self):
        # Lógica de controle para manter a temperatura ambiente
        if self.heating:
            self.sensor_temperature += 0.1
        elif self.cooling:
            self.sensor_temperature -= 0.1

    def set_target_temperature(self, new_target):
        self.target_temperature = new_target

# Funções chamadas pelos botões do menu
def choose_temperature():
    new_target = float(entry_temperature.get())
    system.set_target_temperature(new_target)
    update_temperature_display()

def auto_regulate_temperature():
    system.heating = False
    system.cooling = False

def heat_room():
    system.heating = True
    system.cooling = False

def cool_room():
    system.heating = False
    system.cooling = True

def update_temperature_display():
    current_temperature = system.measure_temperature()
    label_temperature.config(text=f"Temperatura Atual: {current_temperature}°C")
    system.regulate_temperature()
    root.after(1000, update_temperature_display)  # Atualiza a temperatura a cada segundo

# Configuração da janela principal
root = tk.Tk()
root.title("Sistema de Controle de Temperatura")

# Configuração do sistema de controle de temperatura
system = TemperatureControlSystem()

# Configuração dos widgets
label_temperature = tk.Label(root, text="Temperatura Atual: 25.0°C")
entry_temperature = tk.Entry(root)
button_choose_temperature = tk.Button(root, text="Escolher Temperatura", command=choose_temperature)
button_auto_regulate = tk.Button(root, text="Regular Automaticamente", command=auto_regulate_temperature)
button_heat_room = tk.Button(root, text="Aquecer Sala", command=heat_room)
button_cool_room = tk.Button(root, text="Arrefecer Sala", command=cool_room)

# Organização dos widgets na interface
label_temperature.pack(pady=10)
entry_temperature.pack(pady=5)
button_choose_temperature.pack(pady=5)
button_auto_regulate.pack(pady=5)
button_heat_room.pack(pady=5)
button_cool_room.pack(pady=5)

# Iniciar o loop principal da interface gráfica
root.after(1000, update_temperature_display)  # Inicia a atualização da temperatura
root.mainloop()

import random


class TemperatureSensor:
    def __init__(self):
        self.current_temperature = 20.0

    def read_temperature(self):
        variation = random.uniform(-0.5, 0.5)
        self.current_temperature += variation
        return self.current_temperature

class TemperatureController:
    def __init__(self, desired_temperature):
        self.desired_temperature = desired_temperature
        self.target_temperature_range = 1.0
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




import random

from PrintSystem import *

class TemperatureSensor:
    def __init__(self):
         # Initializes temperature sensor with an initial temperature and no variation
        self.current_temperature = 22
        self.temperature_variation = 0

    def read_temperature(self):
        # Adds the variation caused by the controller to the current temperature
        self.current_temperature += self.temperature_variation
        
        return self.current_temperature

    def set_temperature_variation(self, variation):
        # Sets the temperature variation caused by the controller
        self.temperature_variation = variation


class PIDController:
    def __init__(self, setpoint):
        # Initializes PID controller with constants and variables
        self.setpoint = setpoint
        self.Kp = 0.5  # Proportional constant
        self.Ki = 0.2  # Integral constant
        self.Kd = 0.01 # Derivative constant
        self.prev_error = 0.0
        self.integral = 0.0
        self.derivative = 0.0

    def updatePID(self, current_temperature):
        # Updates PID controller based on current temperature and setpoint
        error = self.setpoint - current_temperature

        self.integral += error
        self.derivative = error - self.prev_error

        self.PIDoutput = self.Kp * error + self.Ki * self.integral + self.Kd * self.derivative

        self.prev_error = error


class TemperatureController:
    def __init__(self, temperature_sensor):
        # Initializes temperature controller
        self.desired_temperature = None
        self.pid_controller = PIDController(self.desired_temperature)
        self.temperature_sensor = temperature_sensor
        self.controller_active = False

    def activate_controller(self, desired_temperature):
        # Activates temperature controller with the desired temperature
        self.desired_temperature = desired_temperature
        self.pid_controller.setpoint = desired_temperature
        self.controller_active = True

    def update_temperature(self):
        # Update the temperature based on the PID controller's output
        self.current_temperature = self.temperature_sensor.read_temperature()
        
        if self.controller_active:      # If the controller is active
            self.pid_controller.updatePID(self.current_temperature)

            # Prints PID controller output and current temperature information
            print_PIDoutput(self.pid_controller, self.current_temperature, self.desired_temperature)

            # Adjusts the room temperature based on the PID output
            self.temperature_sensor.set_temperature_variation(self.pid_controller.PIDoutput)            
        else:                           # If the controller is disabled
            # Simulates a real temperature sensor reading with variation
            variation = random.uniform(-0.1, 0.1)

            self.temperature_sensor.set_temperature_variation(variation)

        




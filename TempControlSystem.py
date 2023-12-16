import random


class TemperatureSensor:
    def __init__(self):
        self.current_temperature = 20.0
        self.temperature_variation = 0.0

    def read_temperature(self):
        # Adiciona a variação causada pelo controlador ao valor atual da temperatura
        self.current_temperature += self.temperature_variation

        # Simula uma leitura real do sensor
        variation = random.uniform(-0.5, 0.5)
        self.current_temperature += variation

        return self.current_temperature

    def set_temperature_variation(self, variation):
        # Define a variação de temperatura causada pelo controlador
        self.temperature_variation = variation


class PIDController:
    def __init__(self, setpoint):
        self.setpoint = setpoint
        self.Kp = 0.5  # Constante proporcional
        self.Ki = 0.2  # Constante integral
        self.Kd = 0.01 # Constante derivativa
        self.prev_error = 0.0
        self.integral = 0.0

    def update(self, current_temperature):
        error = self.setpoint - current_temperature
        print(error)

        self.integral += error
        derivative = error - self.prev_error

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        print(output)
        self.prev_error = error

        return output


class TemperatureController:
    def __init__(self, temperature_sensor):
        self.desired_temperature = 25.0
        self.pid_controller = PIDController(self.desired_temperature)
        self.temperature_sensor = temperature_sensor
        self.controller_active = False

    def activate_controller(self, desired_temperature):
        self.desired_temperature = desired_temperature
        self.pid_controller.setpoint = desired_temperature
        self.controller_active = True

    def adjust_temperature(self):
        if self.controller_active:
            current_temperature = self.temperature_sensor.read_temperature()
            pid_output = self.pid_controller.update(current_temperature)

            if pid_output > 0:
                print("Temperature increasing...")
            elif pid_output < 0:
                print("Temperature decreasing...")
            else:
                print("Temperature stable.")

            # Ajustar a temperatura da sala com base na saída do PID
            self.temperature_sensor.set_temperature_variation(pid_output)

            if abs(current_temperature - self.desired_temperature) < 0.1:
                print("Temperature reached the setpoint!")

            

    def set_desired_temperature(self, new_target):
        self.desired_temperature = new_target
        self.pid_controller.setpoint = new_target

    def auto_regulate_temperature(self):
        self.heating = False
        self.cooling = False

    def heat_room(self):
        self.heating = True
        self.cooling = False

    def cool_room(self):
        self.heating = False
        self.cooling = True




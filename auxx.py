from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import sys
from colorama import Fore, Style
import random
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def print_PIDoutput(pid_output, current_temperature, desired_temperature):
    print(Style.BRIGHT + "=     Desired Temperature: " + Fore.YELLOW + f"{desired_temperature:.2f}°C     =" + Style.RESET_ALL)
    
    if pid_output.PIDoutput > 0.01:
        print(Style.BRIGHT + "=     Current Temperature: " + Fore.RED + f"{current_temperature:.2f}°C     =" + Style.RESET_ALL)
        print(Style.BRIGHT + Fore.RED + "=       Temperature increasing...      =" + Style.RESET_ALL)
    elif pid_output.PIDoutput < -0.01:
        print(Style.BRIGHT + "=     Current Temperature: " + Fore.BLUE + f"{current_temperature:.2f}°C     =" + Style.RESET_ALL)
        print(Style.BRIGHT + Fore.BLUE + "=       Temperature decreasing...      =" + Style.RESET_ALL)
    else:
        print(Style.BRIGHT + "=     Current Temperature: " + Fore.GREEN + f"{current_temperature:.2f}°C     =" + Style.RESET_ALL)
        print(Style.BRIGHT + Fore.GREEN + "=          Temperature stable.         =" + Style.RESET_ALL)

    if pid_output.PIDoutput < 0:
        print(Style.BRIGHT + f"=       Controller Error: {pid_output.PIDoutput:.3f}       =" + Style.RESET_ALL)
    else:
        print(Style.BRIGHT + f"=       Controller Error: {pid_output.PIDoutput:.3f}        =" + Style.RESET_ALL)

    print('\n\n')

class FuzzyPIDController:
    def __init__(self):
        # Antecedentes
        self.error = ctrl.Antecedent(np.arange(-5, 5, 1), 'error')
        self.error_derivative = ctrl.Antecedent(np.arange(-5, 5, 1), 'error_derivative')

        # Consequente
        self.output_action = ctrl.Consequent(np.arange(-1, 1, 0.1), 'acao')

        # Universo para a temperatura desejada
        self.desired_temperature = ctrl.Antecedent(np.arange(16, 33, 1), 'temperatura')
        self.desired_temperature['confortavel'] = fuzz.trimf(self.desired_temperature.universe, [20, 23, 26])

        # Funções de pertinência para o erro e sua derivada
        self.error['positive'] = fuzz.trimf(self.error.universe, [0, 5, 5])
        self.error['zero'] = fuzz.trimf(self.error.universe, [-5, 0, 5])
        self.error['negative'] = fuzz.trimf(self.error.universe, [-5, -5, 0])

        self.error_derivative['positive'] = fuzz.trimf(self.error_derivative.universe, [0, 5, 5])
        self.error_derivative['zero'] = fuzz.trimf(self.error_derivative.universe, [-5, 0, 5])
        self.error_derivative['negative'] = fuzz.trimf(self.error_derivative.universe, [-5, -5, 0])

        # Funções de pertinência para a ação de controle
        self.output_action['positive'] = fuzz.trimf(self.output_action.universe, [0, 1, 1])
        self.output_action['zero'] = fuzz.trimf(self.output_action.universe, [-1, 0, 1])
        self.output_action['negative'] = fuzz.trimf(self.output_action.universe, [-1, -1, 0])

        # Regras
        self.rule1 = ctrl.Rule(antecedent=(self.error['negative'] & self.error_derivative['zero']),
                               consequent=self.output_action['positive'])
        self.rule2 = ctrl.Rule(antecedent=(self.error['zero'] & self.error_derivative['zero']),
                               consequent=self.output_action['zero'])
        self.rule3 = ctrl.Rule(antecedent=(self.error['positive'] & self.error_derivative['zero']),
                               consequent=self.output_action['negative'])

        # Sistema de controle
        self.sistema = ctrl.ControlSystem(rules=[self.rule1, self.rule2, self.rule3])
        self.fuzzy_pid_controller = ctrl.ControlSystemSimulation(self.sistema)

    def ajustar_parametros_pid(self):
        kp = self.sistema.output['acao']
        ki = kp
        kd = kp

        self.fuzzy_pid_controller.Kp = kp
        self.fuzzy_pid_controller.Ki = ki
        self.fuzzy_pid_controller.Kd = kd

class TemperatureController:
    def __init__(self, temperature_sensor):
        self.desired_temperature = None
        self.fuzzy_pid_controller = FuzzyPIDController()
        self.temperature_sensor = temperature_sensor
        self.controller_active = False

    def activate_controller(self, desired_temperature):
        self.desired_temperature = desired_temperature
        self.fuzzy_pid_controller.desired_temperature['confortavel'] = desired_temperature
        self.controller_active = True

    def adjust_temperature(self):
        self.current_temperature = self.temperature_sensor.read_temperature()

        if self.controller_active:
            self.fuzzy_pid_controller.sistema.input['temperatura'] = self.current_temperature
            self.fuzzy_pid_controller.sistema.compute()
            self.fuzzy_pid_controller.ajustar_parametros_pid()
            self.temperature_sensor.set_temperature_variation(self.fuzzy_pid_controller.adjust_temperature(self.current_temperature))
        else:
            variation = random.uniform(-0.1, 0.1)
            self.temperature_sensor.set_temperature_variation(variation)

class TemperatureControlApp(QWidget):
    def __init__(self):
        super(TemperatureControlApp, self).__init__()

        self.temp_sensor = TemperatureSensor()
        self.temp_controller = TemperatureController(self.temp_sensor)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Group Box 1 - Display
        group_box1 = QGroupBox("DISPLAY")
        layout1 = QVBoxLayout()

        self.label_temperature = QLabel(f"Current Temperature: {self.temp_sensor.current_temperature:.2f}°C")
        self.label_operation_mode = QLabel("Operation Mode: None")

        layout1.addWidget(self.label_temperature)
        layout1.addWidget(self.label_operation_mode)
        group_box1.setLayout(layout1)

        # Group Box 2 - Operation Modes
        group_box2 = QGroupBox("OPERATION MODES")
        layout2 = QGridLayout()

        self.button_choose_temperature = QPushButton("Choose Temperature")
        self.button_choose_temperature.clicked.connect(self.choose_temperature)

        self.button_auto_regulate = QPushButton("Auto Regulate")
        self.button_auto_regulate.clicked.connect(self.auto_regulate_temperature)

        self.button_heat_room = QPushButton("Increase 1°C")
        self.button_heat_room.clicked.connect(self.heat_room)

        self.button_cool_room = QPushButton("Decrease 1°C")
        self.button_cool_room.clicked.connect(self.cool_room)

        layout2.addWidget(self.button_choose_temperature, 0, 0)  # row 0, column 0
        layout2.addWidget(self.button_auto_regulate, 0, 1)  # row 0, column 1
        layout2.addWidget(self.button_heat_room, 1, 0)  # row 1, column 0
        layout2.addWidget(self.button_cool_room, 1, 1)  # row 1, column 1

        group_box2.setLayout(layout2)

        # Exit Button
        button_exit = QPushButton("Exit")
        button_exit.clicked.connect(self.close)

        # Add Group Boxes to the main layout
        main_layout.addWidget(group_box1)
        main_layout.addWidget(group_box2)
        main_layout.addWidget(button_exit)

        self.setLayout(main_layout)

        # Setup timer for updating temperature every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_temperature_display)
        self.timer.start(1000)  # 1000 milliseconds = 1 second

        # Set background color to light blue
        self.setStyleSheet("background-color: lightblue;")

    def update_temperature_display(self):
        self.temp_controller.adjust_temperature()
        self.label_temperature.setText(f"Current Temperature: {self.temp_sensor.current_temperature:.2f}°C")

    def choose_temperature(self):
        self.min_temp = 16  # Minimum allowed temperature
        self.max_temp = 32  # Maximum allowed temperature

        temperature, ok_button = QInputDialog.getDouble(self, "Choose Temperature", f"Enter desired temperature ({self.min_temp}°C to {self.max_temp}°C):", min=self.min_temp, max=self.max_temp)
        if ok_button:
            QMessageBox.information(self, "Temperature Control System", f"Desired temperature set to {temperature:.2f}°C")
            print(Style.BRIGHT + Fore.LIGHTCYAN_EX + f"=== Mode Choose Temperature ({temperature}°C) ===" + Style.RESET_ALL)
            self.temp_controller.activate_controller(temperature)
            self.label_operation_mode.setText(f"Operation Mode: Choose Temperature ({temperature:.2f}°C)")

    def auto_regulate_temperature(self):
        temperature = 23.0      # Ideal temperature
        self.temp_controller.activate_controller(temperature)
        self.label_operation_mode.setText(f"Operation Mode: Auto Regulate ({temperature:.2f}°C)")
        print(Style.BRIGHT + Fore.LIGHTCYAN_EX + f"===    Mode Auto Regulate ({temperature}°C)   ===" + Style.RESET_ALL)

    def heat_room(self):
        if self.temp_controller.desired_temperature is not None:
            self.temp_controller.desired_temperature += 1.0
            temperature = self.temp_controller.desired_temperature
            self.temp_controller.activate_controller(temperature)
            self.label_operation_mode.setText("Operation Mode: Increase 1°C")
            print(Style.BRIGHT + Fore.LIGHTCYAN_EX + f"===    Mode Increase 1°C: ({temperature}°C)   ===" + Style.RESET_ALL)
        else:
            print(Style.BRIGHT + Fore.LIGHTRED_EX + "===    Choose a temperature first!   ===" + Style.RESET_ALL)

    def cool_room(self):
        if self.temp_controller.desired_temperature is not None:
            self.temp_controller.desired_temperature -= 1.0
            temperature = self.temp_controller.desired_temperature
            self.temp_controller.activate_controller(temperature)
            self.label_operation_mode.setText("Operation Mode: Decrease 1°C")
            print(Style.BRIGHT + Fore.LIGHTCYAN_EX + f"===    Mode Decrease 1°C: ({temperature}°C)   ===" + Style.RESET_ALL)
        else:
            print(Style.BRIGHT + Fore.LIGHTRED_EX + "===    Choose a temperature first!   ===" + Style.RESET_ALL)

class TemperatureSensor:
    def __init__(self):
        self.current_temperature = 22
        self.temperature_variation = 0

    def read_temperature(self):
        self.current_temperature += self.temperature_variation
        return self.current_temperature

    def set_temperature_variation(self, variation):
        self.temperature_variation = variation

class PIDController:
    def __init__(self, setpoint):
        self.setpoint = setpoint
        self.Kp = 0.5  # Constante proporcional
        self.Ki = 0.2  # Constante integral
        self.Kd = 0.01 # Constante derivativa
        self.prev_error = 0.0
        self.integral = 0.0
        self.derivative = 0.0

    def update(self, current_temperature):
        error = self.setpoint - current_temperature
        self.integral += error
        self.derivative = error - self.prev_error
        self.PIDoutput = self.Kp * error + self.Ki * self.integral + self.Kd * self.derivative
        self.prev_error = error

class TemperatureController:
    def __init__(self, temperature_sensor):
        self.desired_temperature = None
        self.fuzzy_pid_controller = FuzzyPIDController()
        self.temperature_sensor = temperature_sensor
        self.controller_active = False

    def activate_controller(self, desired_temperature):
        self.desired_temperature = desired_temperature
        self.fuzzy_pid_controller.desired_temperature['confortavel'] = desired_temperature
        self.controller_active = True

    def adjust_temperature(self):
        self.current_temperature = self.temperature_sensor.read_temperature()
        if self.controller_active:
            self.fuzzy_pid_controller.sistema.input['temperatura'] = self.current_temperature
            self.fuzzy_pid_controller.sistema.compute()
            self.fuzzy_pid_controller.ajustar_parametros_pid()
            self.temperature_sensor.set_temperature_variation(self.fuzzy_pid_controller.fuzzy_pid_controller.adjust_temperature(self.current_temperature))
        else:
            variation = random.uniform(-0.1, 0.1)
            self.temperature_sensor.set_temperature_variation(variation)

def main():
    app = QApplication(sys.argv)
    window = TemperatureControlApp()
    window.setWindowTitle("Temperature Control System")
    window.setGeometry(200, 200, 500, 250)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

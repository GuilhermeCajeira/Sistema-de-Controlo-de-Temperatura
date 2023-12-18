from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

import sys

from TempControlSystem import *
from PrintSystem import *


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setWindowTitle("Configuration Menu")
        self.setGeometry(200, 200, 400, 200)

        self.setup_config_menu()

    def setup_config_menu(self):
        layout = QVBoxLayout()

        # Exterior Temperature
        group_exterior_temp = QGroupBox("Exterior Temperature")
        layout_exterior_temp = QFormLayout()
        self.combo_ext_temp = QComboBox()
        self.combo_ext_temp.addItems(["Cold", "Mild", "Hot"])
        layout_exterior_temp.addRow(self.combo_ext_temp)
        group_exterior_temp.setLayout(layout_exterior_temp)

        # Time of Day
        group_time_of_day = QGroupBox("Time of Day")
        layout_time_of_day = QFormLayout()
        self.combo_morning = QComboBox()
        self.combo_morning.addItems(["Morning", "Afternoon", "Night"])
        layout_time_of_day.addRow(self.combo_morning)
        group_time_of_day.setLayout(layout_time_of_day)

        # Room Division
        group_room_division = QGroupBox("Room Division")
        layout_room_division = QFormLayout()
        self.combo_division = QComboBox()
        self.combo_division.addItems(["Bedroom", "Living Room", "Office", "Amphitheater"])
        layout_room_division.addRow(self.combo_division)
        group_room_division.setLayout(layout_room_division)

        # Buttons
        button_ok = QPushButton("OK")
        button_ok.clicked.connect(self.accept)
        button_cancel = QPushButton("Cancel")
        button_cancel.clicked.connect(self.reject)

        # Add widgets to layout
        layout.addWidget(group_exterior_temp)
        layout.addWidget(group_time_of_day)
        layout.addWidget(group_room_division)
        layout.addWidget(button_ok)
        layout.addWidget(button_cancel)

        self.setLayout(layout)


class TemperatureControlApp(QWidget):
    def __init__(self):
        # Initializes the main application window
        super(TemperatureControlApp, self).__init__()

        # Set background color to light blue
        self.setStyleSheet("background-color: lightblue;")

        # Initializes temperature sensor and controller
        self.temp_sensor = TemperatureSensor()
        self.temp_controller = TemperatureController(self.temp_sensor)

        # Show the configuration dialog
        self.configure_environment()

        # Setup the application window with menu
        self.setup_app()

    
    def configure_environment(self):
        # Create and show the configuration dialog
        config_dialog = ConfigDialog(self)
        result = config_dialog.exec_()

        # Apply configuration based on user choices
        if result == QDialog.Accepted:
            exterior_temp = config_dialog.combo_ext_temp.currentText()

            time_of_day = config_dialog.combo_morning.currentText()

            room_division = config_dialog.combo_division.currentText()

            
            # Set initial temperature based on exterior temperature
            if exterior_temp == "Cold":
                self.temp_sensor.current_temperature = 28.0
            elif exterior_temp == "Mild":
                self.temp_sensor.current_temperature = 22.0
            elif exterior_temp == "Hot":
                self.temp_sensor.current_temperature = 17.0

            if time_of_day == "Morning":
                self.temp_sensor.current_temperature += 2.0
            elif time_of_day == "Afternoon":
                self.temp_sensor.current_temperature += 0.0
            elif time_of_day == "Night":
                self.temp_sensor.current_temperature -= 2.0

            if room_division == "Bedroom":
                self.temp_sensor.current_temperature -= 1.0
            elif room_division == "Living Room":
                self.temp_sensor.current_temperature += 1.0
            elif room_division == "Office":
                self.temp_sensor.current_temperature += 0.0
            elif room_division == "Amphitheater":
                self.temp_sensor.current_temperature -= 2.0

            print_configEnvironment(exterior_temp, time_of_day, room_division, self.temp_sensor.current_temperature)
        else:
            # User pressed "Cancel," close the application
            sys.exit()
        

    def setup_app(self):
        # Initializes the main layout and components
        main_layout = QVBoxLayout()

        # Group Box 1 - Display
        group_box1 = QGroupBox("DISPLAY")
        layout1 = QVBoxLayout()

        # Labels for displaying current temperature and operation mode
        self.label_temperature = QLabel(f"Current Temperature: {self.temp_sensor.current_temperature:.2f}°C")
        self.label_operation_mode = QLabel("Operation Mode: None")

        # Adds labels to the layout
        layout1.addWidget(self.label_temperature)
        layout1.addWidget(self.label_operation_mode)
        group_box1.setLayout(layout1)
        
        # Group Box 2 - Operation Modes
        group_box2 = QGroupBox("OPERATION MODES")
        layout2 = QGridLayout()

        # Buttons for different operation modes
        self.button_choose_temperature = QPushButton("Choose Temperature")
        self.button_choose_temperature.clicked.connect(self.choose_temperature)

        self.button_auto_regulate = QPushButton("Auto Regulate")
        self.button_auto_regulate.clicked.connect(self.auto_regulate_temperature)

        self.button_heat_room = QPushButton("Increase 1°C")
        self.button_heat_room.clicked.connect(self.heat_room)

        self.button_cool_room = QPushButton("Decrease 1°C")
        self.button_cool_room.clicked.connect(self.cool_room)

        # Adds buttons to the layout in a 2x2 grid
        layout2.addWidget(self.button_choose_temperature, 0, 0)  # row 0, column 0
        layout2.addWidget(self.button_auto_regulate, 0, 1)  # row 0, column 1
        layout2.addWidget(self.button_heat_room, 1, 0)  # row 1, column 0
        layout2.addWidget(self.button_cool_room, 1, 1)  # row 1, column 1

        group_box2.setLayout(layout2)

        # Exit Button
        button_exit = QPushButton("Exit")
        button_exit.clicked.connect(self.close)

        # Adds Group Boxes and Exit Button to the main layout
        main_layout.addWidget(group_box1)
        main_layout.addWidget(group_box2)
        main_layout.addWidget(button_exit)

        self.setLayout(main_layout)

        # Setup a timer for updating the temperature display every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_temperature_display)
        self.timer.start(1000)  # 1000 milliseconds = 1 second


    def update_temperature_display(self):
        # Updates the temperature display in the main window
        self.temp_controller.update_temperature()
        self.label_temperature.setText(f"Current Temperature: {self.temp_sensor.current_temperature:.2f}°C")


    def choose_temperature(self):
        # Allows the user to choose a desired temperature
        self.min_temp = 16  # Minimum allowed temperature
        self.max_temp = 32  # Maximum allowed temperature

        temperature, ok_button = QInputDialog.getDouble(self, "Choose Temperature", f"Enter desired temperature ({self.min_temp}°C to {self.max_temp}°C):", min=self.min_temp, max=self.max_temp)
        if ok_button:
            QMessageBox.information(self, "Temperature Control System", f"Desired temperature set to {temperature:.2f}°C")
            print(Style.BRIGHT + Fore.LIGHTCYAN_EX + f"=== Mode Choose Temperature ({temperature}°C) ===" + Style.RESET_ALL)
            
            self.temp_controller.activate_controller(temperature)
            self.label_operation_mode.setText(f"Operation Mode: Choose Temperature ({temperature:.2f}°C)")


    def auto_regulate_temperature(self):
        # Activates auto-regulation mode
        temperature = 23.0      # Ideal temperature
        self.temp_controller.activate_controller(temperature)

        self.label_operation_mode.setText(f"Operation Mode: Auto Regulate ({temperature:.2f}°C)")
        print(Style.BRIGHT + Fore.LIGHTCYAN_EX + f"===    Mode Auto Regulate ({temperature}°C)   ===" + Style.RESET_ALL)


    def heat_room(self):
        # Increases the desired temperature by 1°C
        if self.temp_controller.desired_temperature is not None:
            self.temp_controller.desired_temperature += 1.0
            temperature = self.temp_controller.desired_temperature
            self.temp_controller.activate_controller(temperature)

            self.label_operation_mode.setText("Operation Mode: Increase 1°C")
            print(Style.BRIGHT + Fore.LIGHTCYAN_EX + f"===    Mode Increase 1°C: ({temperature}°C)   ===" + Style.RESET_ALL)
        else:
            print(Style.BRIGHT + Fore.LIGHTRED_EX + "===    Choose a temperature first!   ===" + Style.RESET_ALL)


    def cool_room(self):
        # Decreases the desired temperature by 1°C
        if self.temp_controller.desired_temperature is not None:
            self.temp_controller.desired_temperature -= 1.0
            temperature = self.temp_controller.desired_temperature
            self.temp_controller.activate_controller(temperature)

            self.label_operation_mode.setText("Operation Mode: Decrease 1°C")
            print(Style.BRIGHT + Fore.LIGHTCYAN_EX + f"===    Mode Decrease 1°C: ({temperature}°C)   ===" + Style.RESET_ALL)
        else:
            print(Style.BRIGHT + Fore.LIGHTRED_EX + "===    Choose a temperature first!   ===" + Style.RESET_ALL)


def main():
    # Main function to run the application
    app = QApplication([])
    window = TemperatureControlApp()
    window.setWindowTitle("Temperature Control System")
    window.setGeometry(200, 200, 500, 250)
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
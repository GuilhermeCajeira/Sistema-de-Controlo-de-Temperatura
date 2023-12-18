from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

import sys

from TempControlSystem import *
from PrintSystem import *


class TemperatureControlApp(QWidget):
    def __init__(self):
        # Initializes the main application window
        super(TemperatureControlApp, self).__init__()

        # Initializes temperature sensor and controller
        self.temp_sensor = TemperatureSensor()
        self.temp_controller = TemperatureController(self.temp_sensor)

        # Setup the application window with menu
        self.setup_app()

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

        # Set background color to light blue
        self.setStyleSheet("background-color: lightblue;")


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
    app = QApplication(sys.argv)
    window = TemperatureControlApp()
    window.setWindowTitle("Temperature Control System")
    window.setGeometry(200, 200, 500, 250)
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
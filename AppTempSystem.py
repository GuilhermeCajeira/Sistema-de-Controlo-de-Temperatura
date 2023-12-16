from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

import sys

from TempControlSystem import *


class TemperatureControlApp(QWidget):
    def __init__(self):
        super(TemperatureControlApp, self).__init__()

        self.temperature_sensor = TemperatureSensor()
        self.temp_controller = TemperatureController(25.0)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Group Box 1 - Display and Input
        group_box1 = QGroupBox("Display and Input")
        layout1 = QVBoxLayout()

        self.label_temperature = QLabel("Current Temperature: 20.0°C")
        self.entry_temperature = QLineEdit()
        self.button_choose_temperature = QPushButton("Choose Temperature")
        self.button_choose_temperature.clicked.connect(self.choose_temperature)

        layout1.addWidget(self.label_temperature)
        layout1.addWidget(self.entry_temperature)
        layout1.addWidget(self.button_choose_temperature)

        group_box1.setLayout(layout1)

        # Group Box 2 - Operation Modes
        group_box2 = QGroupBox("Operation Modes")
        layout2 = QVBoxLayout()

        self.button_auto_regulate = QPushButton("Auto Regulate")
        self.button_auto_regulate.clicked.connect(self.auto_regulate_temperature)

        self.button_heat_room = QPushButton("Heat Room")
        self.button_heat_room.clicked.connect(self.heat_room)

        self.button_cool_room = QPushButton("Cool Room")
        self.button_cool_room.clicked.connect(self.cool_room)

        layout2.addWidget(self.button_auto_regulate)
        layout2.addWidget(self.button_heat_room)
        layout2.addWidget(self.button_cool_room)

        group_box2.setLayout(layout2)

        # Add Group Boxes to the main layout
        main_layout.addWidget(group_box1)
        main_layout.addWidget(group_box2)

        # Exit Button
        button_exit = QPushButton("Exit")
        button_exit.clicked.connect(self.close)

        main_layout.addWidget(button_exit)

        self.setLayout(main_layout)

        # Setup timer for updating temperature every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_temperature_display)
        self.timer.start(1000)  # 1000 milliseconds = 1 second

        self.update_temperature_display()  # Initial update

        # Set background color to light blue
        self.setStyleSheet("background-color: lightblue;")

    def choose_temperature(self):
        temperature, ok = QInputDialog.getDouble(self, "Choose Temperature", "Enter desired temperature:")
        if ok:
            self.temp_controller.desired_temperature = temperature
            self.update_temperature_display()
            QMessageBox.information(self, "Temperature Control System", f"Desired temperature set to {temperature}°C")

    def auto_regulate_temperature(self):
        self.temp_controller.auto_regulate_temperature()
        self.update_temperature_display()

    def heat_room(self):
        self.temp_controller.heat_room()
        self.update_temperature_display()

    def cool_room(self):
        self.temp_controller.cool_room()
        self.update_temperature_display()

    def update_temperature_display(self):
        current_temperature = self.temperature_sensor.read_temperature()
        self.label_temperature.setText(f"Current Temperature: {current_temperature:.2f}°C")
        self.temp_controller.adjust_temperature(current_temperature)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TemperatureControlApp()
    window.setWindowTitle("Temperature Control System")
    window.setGeometry(100, 100, 500, 300)
    window.show()
    sys.exit(app.exec_())
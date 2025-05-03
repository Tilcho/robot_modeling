from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import subprocess
import psutil
import sys

# ROS
import rospy
from std_msgs.msg import String, Float64MultiArray

class TouchHMI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("moveitHMI.ui", self)

        # UI-Elemente binden
        self.mainTabWidget = self.findChild(QtWidgets.QTabWidget, "mainTabWidget")
        self.jointTab = self.findChild(QtWidgets.QWidget, "jointTab")
        self.tcpTab = self.findChild(QtWidgets.QWidget, "tcpTab")
        self.displayText = self.findChild(QtWidgets.QLabel, "homeLabel")

        self.autoModeButton = self.findChild(QtWidgets.QPushButton, "autoModeButton")
        self.manualModeButton = self.findChild(QtWidgets.QPushButton, "manualModeButton")
        self.emergencyButton = self.findChild(QtWidgets.QPushButton, "emergencyButton")
        self.acknowledgeButton = self.findChild(QtWidgets.QPushButton, "acknowledgeButton")

        self.joystickUp = self.findChild(QtWidgets.QPushButton, "joystickUp")
        self.joystickDown = self.findChild(QtWidgets.QPushButton, "joystickDown")
        self.joystickLeft = self.findChild(QtWidgets.QPushButton, "joystickLeft")
        self.joystickRight = self.findChild(QtWidgets.QPushButton, "joystickRight")
        self.tcpZUp = self.findChild(QtWidgets.QPushButton, "tcpZUp")
        self.tcpZDown = self.findChild(QtWidgets.QPushButton, "tcpZDown")
        self.tcpYLeft = self.findChild(QtWidgets.QPushButton, "tcpYLeft")
        self.tcpYRight = self.findChild(QtWidgets.QPushButton, "tcpYRight")

        self.jointSelector = self.findChild(QtWidgets.QComboBox, "jointSelector")
        self.jointRobotSelector = self.findChild(QtWidgets.QComboBox, "jointRobotSelector")

        # ROS-Initialisierung
        rospy.init_node("touch_hmi_gui", anonymous=True)
        self.joystick_pub = rospy.Publisher("joystick_cmd", String, queue_size=10)
        rospy.Subscriber("status_lackierer", Float64MultiArray, self.update_joint_display_lackierer)
        rospy.Subscriber("status_uv", Float64MultiArray, self.update_joint_display_uv)

        # Joystick-Signale verbinden
        self.joystickUp.clicked.connect(lambda: self.send_joystick_command("z", "up"))
        self.joystickDown.clicked.connect(lambda: self.send_joystick_command("z", "down"))
        self.joystickLeft.clicked.connect(lambda: self.send_joystick_command("x", "down"))
        self.joystickRight.clicked.connect(lambda: self.send_joystick_command("x", "up"))
        self.tcpZUp.clicked.connect(lambda: self.send_joystick_command("z", "up"))
        self.tcpZDown.clicked.connect(lambda: self.send_joystick_command("z", "down"))
        self.tcpYLeft.clicked.connect(lambda: self.send_joystick_command("y", "down"))
        self.tcpYRight.clicked.connect(lambda: self.send_joystick_command("y", "up"))

        # Modus-Buttons
        self.autoModeButton.clicked.connect(self.set_automatic_mode)
        self.manualModeButton.clicked.connect(self.set_manual_mode)
        self.emergencyButton.clicked.connect(self.trigger_emergency)
        self.acknowledgeButton.clicked.connect(self.acknowledge_emergency)

        self.acknowledgeButton.setEnabled(False)
        self.blinkState = False
        self.blinkTimer = QTimer(self)
        self.blinkTimer.timeout.connect(self.toggle_acknowledge_blink)

        # Startzustand synchronisieren
        if self.is_process_running():
            self.set_automatic_mode()
        else:
            self.reset_to_start_mode()

    def send_joystick_command(self, axis_or_joint, direction):
        robot_idx = self.jointRobotSelector.currentIndex()
        robot_map = {0: "lackierer", 1: "uv"}
        robot_name = robot_map.get(robot_idx, "lackierer")

        tab_index = self.mainTabWidget.currentIndex()
        if tab_index == self.mainTabWidget.indexOf(self.jointTab):
            joint_idx = self.jointSelector.currentIndex()
            joint_name = f"joint_{joint_idx + 1}"
            cmd = f"{robot_name}:joint:{joint_name}:{direction}"
        elif tab_index == self.mainTabWidget.indexOf(self.tcpTab):
            axis = axis_or_joint  # "x", "y", "z"
            cmd = f"{robot_name}:tcp:{axis}:{direction}"
        else:
            return

        self.joystick_pub.publish(String(data=cmd))
        print(f"[Joystick] → {cmd}")

    def update_joint_display_lackierer(self, msg):
        if self.jointRobotSelector.currentIndex() == 0:
            self.set_joint_labels(msg.data)

    def update_joint_display_uv(self, msg):
        if self.jointRobotSelector.currentIndex() == 1:
            self.set_joint_labels(msg.data)

    def set_joint_labels(self, values):
        for i in range(min(6, len(values))):
            label = self.findChild(QtWidgets.QLabel, f"joint{i+1}Value")
            label.setText(f"{values[i]:.2f}°")

    def set_automatic_mode(self):
        self.displayText.setText("Modus: Automatik aktiviert.")

        index_joint = self.mainTabWidget.indexOf(self.jointTab)
        index_tcp = self.mainTabWidget.indexOf(self.tcpTab)
        self.mainTabWidget.setTabEnabled(index_joint, False)
        self.mainTabWidget.setTabEnabled(index_tcp, False)

        for btn in [self.joystickUp, self.joystickDown, self.joystickLeft, self.joystickRight,
                    self.tcpZUp, self.tcpZDown, self.tcpYLeft, self.tcpYRight]:
            btn.setEnabled(False)

        self.autoModeButton.setEnabled(False)
        self.manualModeButton.setEnabled(True)

        if not self.is_process_running():
            subprocess.Popen(["python3", "prozess.py"])
            print("prozess.py gestartet")

    def set_manual_mode(self):
        self.displayText.setText("Modus: Manuell aktiviert.")

        index_joint = self.mainTabWidget.indexOf(self.jointTab)
        index_tcp = self.mainTabWidget.indexOf(self.tcpTab)
        self.mainTabWidget.setTabEnabled(index_joint, True)
        self.mainTabWidget.setTabEnabled(index_tcp, True)

        for btn in [self.joystickUp, self.joystickDown, self.joystickLeft, self.joystickRight,
                    self.tcpZUp, self.tcpZDown, self.tcpYLeft, self.tcpYRight]:
            btn.setEnabled(True)

        self.autoModeButton.setEnabled(True)
        self.manualModeButton.setEnabled(False)

        for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            try:
                if "prozess.py" in proc.info['cmdline']:
                    proc.terminate()
                    print("prozess.py gestoppt")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def reset_to_start_mode(self):
        self.displayText.setText("Modus auswählen:")

        index_joint = self.mainTabWidget.indexOf(self.jointTab)
        index_tcp = self.mainTabWidget.indexOf(self.tcpTab)
        self.mainTabWidget.setTabEnabled(index_joint, True)
        self.mainTabWidget.setTabEnabled(index_tcp, True)

        for btn in [self.joystickUp, self.joystickDown, self.joystickLeft, self.joystickRight,
                    self.tcpZUp, self.tcpZDown, self.tcpYLeft, self.tcpYRight]:
            btn.setEnabled(True)

        self.autoModeButton.setEnabled(True)
        self.manualModeButton.setEnabled(True)
        self.mainTabWidget.setCurrentIndex(0)

    def trigger_emergency(self):
        self.displayText.setText("⚠️ NOT-AUS aktiviert!")
        print("NOT-AUS gedrückt")

        self.acknowledgeButton.setEnabled(True)
        self.blinkTimer.start(500)

    def acknowledge_emergency(self):
        self.displayText.setText("✅ Not-Aus quittiert.")
        print("Not-Aus quittiert")

        self.blinkTimer.stop()
        self.reset_acknowledge_button()
        self.reset_to_start_mode()

    def toggle_acknowledge_blink(self):
        self.blinkState = not self.blinkState
        if self.blinkState:
            self.acknowledgeButton.setStyleSheet("background-color: red; color: white;")
        else:
            self.acknowledgeButton.setStyleSheet("background-color: yellow; color: black;")

    def reset_acknowledge_button(self):
        self.acknowledgeButton.setEnabled(False)
        self.acknowledgeButton.setStyleSheet("""
            background-color: yellow;
            color: black;
            font-size: 16px;
            font-weight: bold;
            min-width: 100px;
            min-height: 50px;
            max-width: 100px;
            max-height: 50px;
            border-radius: 10px;
        """)

    def is_process_running(self, name="prozess.py"):
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            try:
                if name in proc.info['cmdline']:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TouchHMI()
    window.show()
    sys.exit(app.exec_())


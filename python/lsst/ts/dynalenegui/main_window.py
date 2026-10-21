# This file is part of ts_dynalenegui.
#
# Developed for the Vera Rubin Observatory Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__all__ = ["MainWindow"]

import sys

from PySide6.QtCore import QDateTime, Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """Main window of the Dynalene GUI."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Dynalene Control")
        self.setMinimumSize(300, 560)  # width, height

        # Disable maximize and minimize buttons
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
        )

        self._add_tool_bar()

        # Style sheet to mimic classic native desktop look
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e8e8e8;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #b0b0b0;
                border-radius: 4px;
                margin-top: 10px;
                background-color: #f0f0f0;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 4px;
            }
            /* Status Light Square Style */
            QLabel#status_light {
                background-color: #55ff55;
                border: 1px solid #33cc33;
                border-radius: 2px;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #b0b0b0;
                font-size: 13px;
            }
            QListWidget::item:selected {
                background-color: #2b82c5;
                color: #ffffff;
            }
            QPushButton {
                background-color: #e1e1e1;
                border: 1px solid #adadad;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e5f1fb;
                border-color: #0078d7;
            }
        """)

        # Date and Time Container
        date_time_group = QGroupBox()
        date_time_layout = QFormLayout(date_time_group)
        date_time_layout.setLabelAlignment(Qt.AlignLeft)

        self.date_label = QLabel()
        self.time_label = QLabel()

        date_time_layout.addRow("Date:", self.date_label)
        date_time_layout.addRow("Time:", self.time_label)

        # Summary Container
        summary_group = QGroupBox("Summary")
        summary_layout = QFormLayout(summary_group)
        summary_layout.setLabelAlignment(Qt.AlignLeft)

        # System Status Text + Status Light Container
        self.system_state = QLabel("INITIALIZED")

        self.status_light = QLabel()
        self.status_light.setObjectName("status_light")
        self.status_light.setFixedSize(60, 16)  # Width, Height

        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(8)

        status_layout.addWidget(self.system_state)
        status_layout.addWidget(self.status_light)
        status_layout.addStretch()  # Keeps light next to the text

        # User Profile and Dropdown
        self.selected_user = QLabel("Operator")
        self.select_user = QComboBox()
        self.select_user.addItems(["Operator", "Engineer", "Admin"])

        # Add fields to Summary box
        summary_layout.addRow("System State:", status_container)
        summary_layout.addRow("User Profile:", self.selected_user)
        summary_layout.addRow("Users:", self.select_user)

        # Action Buttons
        self.switch_user = QPushButton("Switch User")
        self.logout = QPushButton("Logout")

        # Command / Action List Box
        self.command_list = QListWidget()
        commands = [
            "General Commands",
            "Commands",
            "Alarms",
            "Cabinet Management",
            "Thermal Summary",
            "User Interface (UI)",
            "Air Handling",
            "PID",
            "Sensors",
            "Chillers & Pumps",
            "Configurations",
            "Errors",
            "Logs",
        ]
        self.command_list.addItems(commands)
        self.command_list.setCurrentRow(0)

        # Connect signals
        self.switch_user.clicked.connect(self.handle_switch_user)
        self.logout.clicked.connect(self.handle_logout)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 10)
        main_layout.setSpacing(10)

        main_layout.addWidget(date_time_group)
        main_layout.addWidget(summary_group)
        main_layout.addWidget(self.switch_user)
        main_layout.addWidget(self.logout)
        main_layout.addWidget(self.command_list)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Setup clock timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

    def update_clock(self) -> None:
        now = QDateTime.currentDateTime()
        self.date_label.setText(now.toString("MM/dd/yy"))
        self.time_label.setText(now.toString("hh:mm AP"))

    def handle_switch_user(self) -> None:
        current_selection = self.select_user.currentText()
        self.selected_user.setText(current_selection)

    def handle_logout(self) -> None:
        print("Logout clicked")

    def _add_tool_bar(self) -> None:
        """Add the tool bar."""

        tool_bar = self.addToolBar("ToolBar")

        action_exit = tool_bar.addAction("Exit", self._handle_exit)
        action_exit.setToolTip("Exit the application")

        action_connect = tool_bar.addAction("Connect", self._handle_connect)
        action_connect.setToolTip("Connect to the dynalene controller")

        action_disconnect = tool_bar.addAction("Disconnect", self._handle_disconnect)
        action_disconnect.setToolTip("Disconnect and close all tasks")

        action_settings = tool_bar.addAction("Settings", self._handle_settings)
        action_settings.setToolTip("Show the application settings")

    def _handle_exit(self) -> None:
        """Exit the application."""

        reply = QMessageBox.question(
            self,
            "Exit Confirmation",  # Window Tittle
            "Are you sure you want to exit?",  # Message Text
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.No,  # Default focused button
        )

        # Check wich button the user clicked
        if reply == QMessageBox.StandardButton.Yes:
            print("Exiting...")
            sys.exit()
        else:
            print("Not exiting...")

    def _handle_connect(self) -> None:
        """Connect to the dynalene controller."""

        print("Connect action triggered")

    def _handle_disconnect(self) -> None:
        """Disconnect from the dynalene controller."""

        print("Disconnect action triggered")

    def _handle_settings(self) -> None:
        """Show the application settings."""

        print("Settings action triggered")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

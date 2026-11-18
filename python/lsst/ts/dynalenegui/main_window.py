# This file is part of ts_dynalenegui.
#
# Developed for the Vera C. Rubin Observatory Telescope and Site Systems.
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

__all__ = ["MainWindow"]

import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from lsst.ts.guitool import TabTemplate

from .control_panel import ControlPanel
from .tab import (
    TabAirHandling,
    TabAlarms,
    TabCabinetManagement,
    TabChillersPumps,
    TabCommand,
    TabConfigurations,
    TabErrors,
    TabGeneralCommands,
    TabLogs,
    TabPid,
    TabSensors,
    TabThermalSummary,
    TabUserInterface,
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

        # Control Panel
        self._control_panel = ControlPanel(logging.getLogger())

        # Command List
        tabs: list[TabTemplate] = [
            TabGeneralCommands("General Commands"),
            TabCommand("Commands"),
            TabAlarms("Alarms"),
            TabCabinetManagement("Cabinet Management"),
            TabThermalSummary("Thermal Summary"),
            TabUserInterface("User Interface (UI)"),
            TabAirHandling("Air Handling"),
            TabPid("PID"),
            TabSensors("Sensors"),
            TabChillersPumps("Chillers & Pumps"),
            TabConfigurations("Configurations"),
            TabErrors("Errors"),
            TabLogs("Logs"),
        ]

        self._tabs = {tab.windowTitle(): tab for tab in tabs}

        self.command_list = QListWidget()
        self.command_list.addItems(list(self._tabs))
        self.command_list.setCurrentRow(0)
        self.command_list.itemDoubleClicked.connect(self._handle_show_tab)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 10)
        main_layout.setSpacing(10)
        main_layout.addWidget(self._control_panel)
        main_layout.addWidget(self.command_list)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def _handle_show_tab(self, item: QListWidgetItem) -> None:
        """Show the window of the double-clicked item.
        Parameters
        ----------
        item : `PySide6.QtWidgets.QListWidgetItem`
            Double-clicked item.
        """
        tab = self._tabs.get(item.text())
        if tab is None:
            print(f"Not implemented yet: {item.text()}")
            return
        tab.show()
        tab.raise_()

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

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
import pathlib
import sys
from datetime import datetime

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
    """Main window of the Dynalene GUI.

    Parameters
    ----------
    is_output_log_to_file : `bool`
        Is outputting the log messages to file or not.
    is_output_log_on_screen : `bool`
        Is outputting the log messages on screen or not.
    log : `logging.Logger` or None, optional
        A logger. If None, a logger will be instantiated. (the default is
        None)
    log_level : `int`, optional
        Logging level. (the default is `logging.WARN`)

    Attributes
    ----------
    log : `logging.Logger`
        A logger.
    """

    def __init__(
        self,
        is_output_log_to_file: bool,
        is_output_log_on_screen: bool,
        log: logging.Logger | None = None,
        log_level: int = logging.WARN,
    ) -> None:
        super().__init__()

        # Set the logger
        message_format = "%(asctime)s, %(levelname)s, %(message)s"
        self.log = self._set_log(
            message_format,
            is_output_log_to_file,
            is_output_log_on_screen,
            log_level,
            log=log,
        )

        self.setWindowTitle("Dynalene Control")
        self.setMinimumSize(300, 560)  # width, height

        # Disable the Qt close button
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
        )

        self._add_tool_bar()

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
        self._control_panel = ControlPanel(self.log)

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
        self.command_list.itemDoubleClicked.connect(self._callback_show_tab)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 10)
        main_layout.setSpacing(10)
        main_layout.addWidget(self._control_panel)
        main_layout.addWidget(self.command_list)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def _set_log(
        self,
        message_format: str,
        is_output_log_to_file: bool,
        is_output_log_on_screen: bool,
        level: int,
        log: logging.Logger | None = None,
    ) -> logging.Logger:
        """Set the logger.

        Parameters
        ----------
        message_format : `str`
            Format of the message.
        is_output_log_to_file : `bool`
            Is outputting the log messages to file or not.
        is_output_log_on_screen : `bool`
            Is outputting the log messages on screen or not.
        level : `int`
            Logging level.
        log : `logging.Logger` or None, optional
            A logger. If None, a logger will be instantiated. (the default is
            None)

        Returns
        -------
        log : `logging.Logger`
            A logger.
        """

        if log is None:
            log = logging.getLogger(type(self).__name__)
        else:
            log = log.getChild(type(self).__name__)

        if is_output_log_to_file:
            logging.basicConfig(
                filename=self._get_log_file_name(),
                format=message_format,
            )
        else:
            logging.basicConfig(
                format=message_format,
            )

        if is_output_log_on_screen:
            log.addHandler(logging.StreamHandler(sys.stdout))

        log.setLevel(level)

        return log

    def _get_log_file_name(self, default_log_dir: str = "/rubin/dynalene/log") -> pathlib.Path:
        """Get the log file name.

        Parameters
        ----------
        default_log_dir : `str`, optional
            Default log directory. (the default is "/rubin/dynalene/log")

        Returns
        -------
        `pathlib.Path`
            Log file name.
        """

        log_dir = pathlib.Path(default_log_dir)
        if not log_dir.is_dir():
            print(
                (f"Default log directory: {default_log_dir} does not exist. Use the home directory instead.")
            )
            log_dir = pathlib.Path.home()

        name = "log_%s.txt" % datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

        return log_dir / name

    def _callback_show_tab(self, item: QListWidgetItem) -> None:
        """Show the window of the double-clicked item.

        Parameters
        ----------
        item : `PySide6.QtWidgets.QListWidgetItem`
            Double-clicked item.
        """

        tab = self._tabs.get(item.text())
        if tab is None:
            self.log.warning(f"Not implemented yet: {item.text()}")
            return
        tab.show()
        tab.raise_()

    def _add_tool_bar(self) -> None:
        """Add the tool bar."""

        tool_bar = self.addToolBar("ToolBar")

        action_exit = tool_bar.addAction("Exit", self._callback_exit)
        action_exit.setToolTip("Exit the application")

        action_connect = tool_bar.addAction("Connect", self._callback_connect)
        action_connect.setToolTip("Connect to the dynalene controller")

        action_disconnect = tool_bar.addAction("Disconnect", self._callback_disconnect)
        action_disconnect.setToolTip("Disconnect and close all tasks")

        action_settings = tool_bar.addAction("Settings", self._callback_settings)
        action_settings.setToolTip("Show the application settings")

    def _callback_exit(self) -> None:
        """Exit the application."""

        reply = QMessageBox.question(
            self,
            "Exit Confirmation",  # Window Title
            "Are you sure you want to exit?",  # Message Text
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.No,  # Default focused button
        )

        # Check which button the user clicked
        if reply == QMessageBox.StandardButton.Yes:
            self.log.info("Exiting the application.")
            sys.exit()

    def _callback_connect(self) -> None:
        """Connect to the dynalene controller."""

        self.log.info("Connect action triggered.")

    def _callback_disconnect(self) -> None:
        """Disconnect from the dynalene controller."""

        self.log.info("Disconnect action triggered.")

    def _callback_settings(self) -> None:
        """Show the application settings."""

        self.log.info("Settings action triggered.")

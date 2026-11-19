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

__all__ = ["ControlPanel"]

import logging

from PySide6.QtCore import QDateTime, Qt, QTimer
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from lsst.ts.guitool import create_group_box, create_label, set_button


class ControlPanel(QWidget):
    """Control panel.

    Parameters
    ----------
    log : `logging.Logger`
        A logger.

    Attributes
    ----------
    log : `logging.Logger`
        A logger.
    """

    def __init__(self, log: logging.Logger) -> None:
        super().__init__()

        self.log = log

        self._labels = {
            "date": create_label(),
            "time": create_label(),
            "system_state": create_label("INITIALIZED"),
            "status_light": create_label(),
            "user_profile": create_label("Operator"),
        }
        self._labels["status_light"].setObjectName("status_light")
        self._labels["status_light"].setFixedSize(60, 16)

        self._combo_box_user = QComboBox()
        self._combo_box_user.addItems(["Operator", "Engineer", "Admin"])

        self._button_switch_user = set_button("Switch User", self._callback_switch_user)
        self._button_logout = set_button("Logout", self._callback_logout)

        self.setLayout(self._create_layout())

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_clock)
        self._timer.start(1000)
        self._update_clock()

    def _create_layout(self) -> QVBoxLayout:
        """Create the layout.

        Returns
        -------
        layout : `PySide6.QtWidgets.QVBoxLayout`
            Layout.
        """

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._create_group_date_time())
        layout.addWidget(self._create_group_summary())
        layout.addWidget(self._button_switch_user)
        layout.addWidget(self._button_logout)

        return layout

    def _create_group_date_time(self) -> QGroupBox:
        """Create the group of date and time.

        Returns
        -------
        `PySide6.QtWidgets.QGroupBox`
            Group.
        """

        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)

        layout.addRow("Date:", self._labels["date"])
        layout.addRow("Time:", self._labels["time"])

        return create_group_box("", layout)

    def _create_group_summary(self) -> QGroupBox:
        """Create the group of summary.

        Returns
        -------
        `PySide6.QtWidgets.QGroupBox`
            Group.
        """

        # System state text + status light, side by side
        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(8)

        status_layout.addWidget(self._labels["system_state"])
        status_layout.addWidget(self._labels["status_light"])
        status_layout.addStretch()  # Keeps status light next to the text

        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)

        layout.addRow("System State:", status_container)
        layout.addRow("User Profile:", self._labels["user_profile"])
        layout.addRow("Users:", self._combo_box_user)

        return create_group_box("Summary", layout)

    def _update_clock(self) -> None:
        """Update the clock."""

        now = QDateTime.currentDateTime()
        self._labels["date"].setText(now.toString("MM/dd/yy"))
        self._labels["time"].setText(now.toString("hh:mm AP"))

    def _callback_switch_user(self) -> None:
        """Callback to switch user profile."""

        user = self._combo_box_user.currentText()
        self._labels["user_profile"].setText(user)
        self.log.info(f"Switched user to {user}.")

    def _callback_logout(self) -> None:
        """Callback to logout."""

        self.log.info("Logout clicked.")

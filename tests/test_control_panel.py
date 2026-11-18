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

import logging

import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from lsst.ts.dynalenegui import ControlPanel


@pytest.fixture
def widget(qtbot: QtBot) -> ControlPanel:
    widget = ControlPanel(logging.getLogger())
    qtbot.addWidget(widget)

    return widget


def test_init(widget: ControlPanel) -> None:
    assert len(widget._labels) == 5
    assert widget._labels["user_profile"].text() == "Operator"


def test_update_clock(widget: ControlPanel) -> None:
    assert widget._labels["date"].text() != ""
    assert widget._labels["time"].text() != ""


def test_callback_switch_user(qtbot: QtBot, widget: ControlPanel) -> None:
    widget._combo_box_user.setCurrentText("Engineer")
    qtbot.mouseClick(widget._button_switch_user, Qt.LeftButton)

    assert widget._labels["user_profile"].text() == "Engineer"

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

import pytest
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from lsst.ts.dynalenegui import MainWindow


@pytest.fixture
def widget(qtbot: QtBot) -> MainWindow:
    widget = MainWindow()
    qtbot.addWidget(widget)

    return widget


def test_command_list(widget: MainWindow) -> None:
    assert widget.command_list.count() == 13
    assert widget.command_list.item(1).text() == "Commands"


def test_double_click_opens_tab(qtbot: QtBot, widget: MainWindow) -> None:
    with qtbot.waitExposed(widget):
        widget.show()

    tab = widget._tabs["Commands"]
    assert tab.isVisible() is False

    item = widget.command_list.item(1)
    position = widget.command_list.visualItemRect(item).center()
    viewport = widget.command_list.viewport()
    qtbot.mouseClick(viewport, Qt.LeftButton, pos=position)
    qtbot.mouseDClick(viewport, Qt.LeftButton, pos=position)

    assert tab.isVisible() is True
    assert tab.windowTitle() == "Commands"

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

__all__ = ["run_dynalenegui"]

import sys

from PySide6.QtCore import QCommandLineOption, QCommandLineParser
from PySide6.QtWidgets import QApplication

from .main_window import MainWindow


def run_dynalenegui() -> None:
    """Run the Dynalene GUI application."""

    app = QApplication(sys.argv)
    app.setApplicationName("Dynalene EUI")

    parser, options = create_parser()
    parser.process(app)  # Handles -h and invalid options, then exits

    is_verbose = parser.isSet(options[0])
    log_level = int(parser.value(options[1]))
    is_output_log_to_file = not parser.isSet(options[2])

    window_main = MainWindow(is_output_log_to_file, is_verbose, log_level=log_level)
    window_main.show()

    sys.exit(app.exec())


def create_parser() -> tuple[QCommandLineParser, list[QCommandLineOption]]:
    """Create the command line parser.

    Returns
    -------
    parser : `PySide6.QtCore.QCommandLineParser`
        Command line parser.
    `list` [`PySide6.QtCore.QCommandLineOption`]
        List of command line options.
    """

    parser = QCommandLineParser()
    parser.setApplicationDescription("Run the Dynalene graphical user interface (GUI).")
    parser.addHelpOption()

    option_verbose = QCommandLineOption(["v", "verbose"], "Print log messages to terminal.")
    parser.addOption(option_verbose)

    option_log_level = QCommandLineOption(
        ["d", "debuglevel"],
        (
            "Debug logging level: CRITICAL (50), ERROR (40), WARNING (30), "
            "INFO (20), DEBUG (10), NOTSET (0). The default is 20."
        ),
        "level",
        "20",
    )
    parser.addOption(option_log_level)

    option_no_log_file = QCommandLineOption(["no-logfile"], "Do not write log messages to file.")
    parser.addOption(option_no_log_file)

    return parser, [
        option_verbose,
        option_log_level,
        option_no_log_file,
    ]

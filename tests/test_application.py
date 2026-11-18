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

import shutil
import subprocess


def test_run_dynalenegui() -> None:
    # Make sure the application is installed
    exe_path = shutil.which("run_dynalenegui")
    assert exe_path is not None

    # Run it with -h: it prints the help and exits without opening a window
    result = subprocess.run([exe_path, "-h"], capture_output=True, text=True, timeout=30)

    assert result.returncode == 0
    assert "--debuglevel" in result.stdout

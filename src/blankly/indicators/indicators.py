"""
    Tulipy wrappers
    Copyright (C) 2021 Brandon Fan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pandas as pd

try:
    import tulipy as ti
    TULIPY_AVAILABLE = True
except ImportError:
    TULIPY_AVAILABLE = False
    ti = None

from blankly.indicators.utils import check_series, convert_to_numpy


def _check_tulipy():
    if not TULIPY_AVAILABLE:
        raise ImportError(
            "tulipy is not installed. Install it with: pip install 'blankly[indicators]' "
            "Note: tulipy is not compatible with Python 3.13+"
        )


def bbands(data, period=14, stddev=2):
    _check_tulipy()
    data = convert_to_numpy(data)
    return ti.bbands(data, period, stddev)


def wad(high_data, low_data, close_data, use_series=False):
    _check_tulipy()
    if check_series(high_data) or check_series(low_data) or check_series(close_data):
        use_series = True
    high_data = convert_to_numpy(high_data)
    low_data = convert_to_numpy(low_data)
    close_data = convert_to_numpy(close_data)
    wad = ti.wad(high_data, low_data, close_data)
    return pd.Series(wad) if use_series else wad


def wilders(data, period=50, use_series=False):
    if check_series(data):
        use_series = True
    data = convert_to_numpy(data)
    wilders = ti.wilders(data, period)
    return pd.Series(wilders) if use_series else wilders


def willr(high_data, low_data, close_data, period=50, use_series=False):
    if check_series(high_data) or check_series(low_data) or check_series(close_data):
        use_series = True
    high_data = convert_to_numpy(high_data)
    low_data = convert_to_numpy(low_data)
    close_data = convert_to_numpy(close_data)
    willr = ti.willr(high_data, low_data, close_data, period)
    return pd.Series(willr) if use_series else willr


def true_range(high_data, low_data, close_data, use_series=False):
    if check_series(high_data) or check_series(low_data) or check_series(close_data):
        use_series = True
    high_data = convert_to_numpy(high_data)
    low_data = convert_to_numpy(low_data)
    close_data = convert_to_numpy(close_data)
    tr = ti.tr(high_data, low_data, close_data)
    return pd.Series(tr) if use_series else tr


def average_true_range(high_data, low_data, close_data, period=50, use_series=False):
    if check_series(high_data) or check_series(low_data) or check_series(close_data):
        use_series = True
    high_data = convert_to_numpy(high_data)
    low_data = convert_to_numpy(low_data)
    close_data = convert_to_numpy(close_data)
    atr = ti.atr(high_data, low_data, close_data, period=period)
    return pd.Series(atr) if use_series else atr

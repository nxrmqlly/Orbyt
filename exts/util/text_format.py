#
# This file is part of Orbyt. (https://github.com/nxmrqlly/orbyt)
# Copyright (c) 2023-present Ritam Das
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
For formatting stuff
"""

import logging

from termcolor import colored


def spaced_padding(text, width=50, padding="-") -> str:
    """
    Formats the given `text` by adding padding on both sides.

    Parameters
    -----------
    text: :class:`str`
        The text to format.
    width: :class:`int`
        The width of the text.
    padding: :class:`str`
        The padding to use.

    Returns
    --------
    :class:`str`
        The formatted text.
    """
    text_length = len(text)
    total_padding = width - text_length - 2
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding

    f_tx = f"{padding * left_padding} {text} {padding * right_padding}"
    return f_tx


def truncate(string: str, width: int = 50) -> str:
    """
    Truncates the given `text` to the given `width`.

    Parameters
    -----------
    text: :class:`str`
        The text to truncate.
    width: :class:`int`
        The width of the text.

    Returns
    --------
    :class:`str`
        The truncated text.
    """

    if len(string) > width:
        string = string[: width - 3] + "..."
    return string


class CustomFormatter(logging.Formatter):
    """
    Formatter for console logging

    Parameters
    -----------
    _fmt: :class:`str`
        The format

    _dt_fmt: :class:`str`
        The date format

    _style: :class:`str`
        The style
    """

    def __init__(self, _fmt, _dt_fmt, _style, *args, **kwargs):
        super().__init__(_fmt, _dt_fmt, _style, *args, **kwargs)

        self.formats = {
            logging.DEBUG: colored(_fmt, "dark_grey"),
            logging.INFO: colored(_fmt, "green"),
            logging.WARNING: colored(_fmt, "yellow"),
            logging.ERROR: colored(_fmt, "red"),
            logging.CRITICAL: colored(_fmt, "red", attrs=["bold"]),
        }
        self.datefmt = _dt_fmt
        self.style = _style

    def format(self, record):
        """
        Format the stream

        Parameters
        -----------

        record: :class:`logging.LogRecord`
            The log record
        """
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt, self.datefmt, self.style)
        return formatter.format(record)

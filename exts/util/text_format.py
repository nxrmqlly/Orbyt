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

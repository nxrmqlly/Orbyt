"""
For formatting text

Functions:
    spaced_padding(text, width=50, padding="-")

Classes:
    CustomFormatter
"""

import logging

from termcolor import colored


def spaced_padding(text, width=50, padding="-") -> str:
    """Formats the given `text` by adding padding on both sides.

    Parameters
    ----------
    text : str
        The text to format.
    width : int
        total width of the text (Default value = 50)
    padding : str
        padding character (Default value = "-")

    Returns
    -------


    """
    text_length = len(text)
    total_padding = width - text_length - 2
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding

    f_tx = f"{padding * left_padding} {text} {padding * right_padding}"
    return f_tx


class CustomFormatter(logging.Formatter):
    """Formatter for console logging"""

    def __init__(self, _fmt, _dt_fmt, _style, *args, **kwargs):
        """
        Initializes a new instance of the class.

        Parameters:
            _fmt (str): The format string for the log message.
            _dt_fmt (str): The format string for the log timestamp.
            _style (str): The log style.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
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

        Parameters
        ----------
        record :


        Returns
        -------


        """
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt, self.datefmt, self.style)
        return formatter.format(record)

"""
For formatting text

Functions:
    spaced_padding(text, width=50, padding="-")

Classes:
    CustomFormatter
"""

import logging

from termcolor import colored


def spaced_padding(text, width=50, padding="-"):
    """
    Formats the given `text` by adding padding on both sides.

    Parameters:
        text (str): The text to be formatted.
        width (int): The total width of the formatted text. Default is 50.
        padding (str): The character used for padding. Default is "-".

    Returns:
        str: The formatted text with padding on both sides.
    """
    text_length = len(text)
    total_padding = width - text_length - 2  # Subtract 2 for the spaces around the word
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding

    formatted_text = f"{padding * left_padding} {text} {padding * right_padding}"
    return formatted_text


class CustomFormatter(logging.Formatter):
    def __init__(self, _fmt, _dt_fmt, _style, *args, **kwargs):
        super().__init__(_fmt, _dt_fmt, _style, *args, **kwargs)

        self.FORMATS = {
            logging.DEBUG: colored(_fmt, "dark_grey"),
            logging.INFO: colored(_fmt, "green"),
            logging.WARNING: colored(_fmt, "yellow"),
            logging.ERROR: colored(_fmt, "red"),
            logging.CRITICAL: colored(_fmt, "red", attrs=["bold"]),
        }
        self.datefmt = _dt_fmt
        self.style = _style

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, self.datefmt, self.style)
        return formatter.format(record)

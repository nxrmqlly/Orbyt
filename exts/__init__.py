"""(Biolerplate) To Find Extensions In ./exts/**

Attributes:
    EXTENSIONS (list): List of extensions present
"""
from pkgutil import iter_modules

EXTENSIONS = [module.name for module in iter_modules(__path__, f"{__package__}.")]

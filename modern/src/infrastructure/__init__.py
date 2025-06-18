"""Infrastructure layer for TKA Desktop."""

# API infrastructure exports
try:
    from .api import *
except ImportError:
    # API infrastructure not available
    pass

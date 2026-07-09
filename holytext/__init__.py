__version__ = "0.0.4"
__all__ = [
    "reverse",
    "upper_first",
    "count_words",
    "is_palindrome",
    "truncate",
    "slugify",
    "love",
    "birthday"
]

from .transform import reverse, upper_first
from .analyze import count_words, is_palindrome
from .format import truncate, slugify
from .l_magic import love
from .b_magic import birthday

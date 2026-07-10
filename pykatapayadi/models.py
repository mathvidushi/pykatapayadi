"""
models.py

Data models used by pykatapayadi.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class KatapayadiResult:

    success: bool = False

    word: str = ""

    counted_letters: List[str] = field(default_factory=list)

    ignored_letters: List[str] = field(default_factory=list)

    digits: List[int] = field(default_factory=list)

    reversed_digits: List[int] = field(default_factory=list)

    number: Optional[int] = None

    valid_date: bool = False

    date: str = ""

    trace: List[str] = field(default_factory=list)

    message: str = ""

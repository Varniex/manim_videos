from __future__ import annotations

from manimlib.constants import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from manimlib.typing import ManimColor

# Colors
NAVY_BLUE: ManimColor = "#0066CC"
DARK_BLUE: ManimColor = "#2A9DF4"
VIOLET: ManimColor = "#EE82EE"
INDIGO: ManimColor = "#4B0082"
VIBGYOR: List[ManimColor] = [VIOLET, INDIGO, BLUE, GREEN, YELLOW, ORANGE, RED]

from dataclasses import dataclass
from typing import List

from user import User


@dataclass
class Order:
    user: User
    pills: List[str]

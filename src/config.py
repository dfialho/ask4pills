from dataclasses import dataclass
from typing import List, Dict

from dataclasses_json import dataclass_json

from user import User


@dataclass_json
@dataclass
class Config:
    users: Dict[str, User]
    telegram: 'TelegramConfig'
    lab: 'LabConfig'


@dataclass_json
@dataclass
class TelegramConfig:
    token: str
    allowed_chats: List[int]


@dataclass_json
@dataclass
class LabConfig:
    username: str
    password: str
    sns_email: str

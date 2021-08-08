from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class User:
    name: str
    sns_number: str

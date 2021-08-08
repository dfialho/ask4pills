"""Ask4Pills
Usage:
  server.py -c <config-file> [--dry-run]
  server.py (-h | --help)
  server.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --dry-run     Use a dummy lab.
"""
import json

from docopt import docopt

from config import Config
from lab.dummy import DummyLab
from lab.sns_email import SNSEmailLab
from pharmacist.polite import PolitePharmacist
from pharmacy.telegram import TelegramPharmacy

if __name__ == '__main__':
    args = docopt(__doc__, version='Ask4Pills')
    config_file = args["<config-file>"]

    with open(config_file, "r") as file:
        config = Config.from_dict(json.load(file))

    if args["--dry-run"]:
        lab = DummyLab()
    else:
        lab = SNSEmailLab(
            config.lab.username,
            config.lab.password,
            config.lab.sns_email
        )

    TelegramPharmacy(pharmacist=PolitePharmacist(config.users, lab)).run_forever()

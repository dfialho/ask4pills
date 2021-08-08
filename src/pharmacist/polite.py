from typing import List, Dict

from pharmacist.errors import PharmacistError
from pharmacist.pharmacist import Pharmacist
from lab.lab import Lab
from lab.order import Order
from user import User


class PolitePharmacist(Pharmacist):
    class Cart:
        def __init__(self, user: User):
            self._user = user
            self._pills = []

        def add(self, pill: str):
            self._pills.append(pill)

        def to_order(self) -> Order:
            return Order(self._user, self._pills)

        @property
        def pills(self) -> List[str]:
            return self._pills

        @property
        def user(self) -> User:
            return self._user

    def __init__(self, users: Dict[str, User], lab: Lab):
        self._pharmacy = lab
        self._cart = None
        self._users = users

    def start(self, user_id: str) -> str:
        if self._cart:
            raise PharmacistError(f"An order is on going for user '{self._cart.user.name}' with pills:\n" +
                                  "\n".join(self._cart.pills))

        if user_id not in self._users:
            return f"No user registered with id '{user_id}'. " \
                   f"Available options are: {self._users}"

        user = self._users[user_id]
        self._cart = self.Cart(user)
        return f"Which pills do you want to order?"

    def add_pill(self, pill: str) -> str:
        self._check_order_is_started()
        self._cart.add(pill)
        return f"Cart:\n" + "\n".join(self._cart.pills)

    def cancel(self) -> str:
        self._check_order_is_started()
        self._cart = None
        return f"Cancelled order"

    def ask(self):
        self._check_order_is_started()
        self._pharmacy.order(self._cart.to_order())
        self._cart = None
        return f"Order submitted"

    def _check_order_is_started(self):
        if not self._cart:
            raise PharmacistError("No order has been started")

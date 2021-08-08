from lab.lab import Lab
from lab.order import Order


class DummyLab(Lab):
    def order(self, order: Order):
        print(f"Submitted order: {order}")

import smtplib

from lab.lab import Lab
from lab.order import Order


class SNSEmailLab(Lab):
    def __init__(self, email_user: str, email_pass: str, destination_email: str) -> None:
        self._email_user = email_user
        self._email_pass = email_pass
        self._destination_email = destination_email

    def order(self, order: Order):
        print(f"Submitting order: {order}")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.ehlo()
            server.login(self._email_user, self._email_pass)
            server.sendmail(
                from_addr=self._email_user,
                to_addrs=[self._destination_email],
                msg=self._render_message(order)
            )

    def _render_message(self, order: Order):
        pills_list = "\r\n".join(map(lambda pill: f"- {pill}", order.pills))
        subject = f"{order.user.name.upper()}, SNS {order.user.sns_number} - Medicação"
        return f"""\
From: {self._email_user}
To: {self._destination_email}
Subject: {subject}

Boa tarde,

Venho requerer prescrição médica para os seguintes medicamentos para {order.user.name}, SNS {order.user.sns_number}.

{pills_list}

Médica de família: Dra. Filipa Guerra

Obrigado,

David Fialho
""".encode("utf8")

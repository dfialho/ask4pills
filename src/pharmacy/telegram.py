import logging
from typing import List

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext

from pharmacist.errors import PharmacistError
from pharmacist.pharmacist import Pharmacist
from pharmacy.pharmacy import Pharmacy


class TelegramPharmacy(Pharmacy):
    logger = logging.getLogger(__name__)

    def __init__(self, token: str, allowed_chats: List[int], pharmacist: Pharmacist) -> None:
        self._allowed_chats = allowed_chats
        self._token = token
        self._pharmacist = pharmacist

    def run_forever(self) -> None:
        updater = Updater(token=self._token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', self.__start, pass_args=True))
        dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.__add_pill))
        dispatcher.add_handler(CommandHandler('cancel', self.__cancel))
        dispatcher.add_handler(CommandHandler('ask', self.__ask))
        self.logger.info("Running...")
        updater.start_polling()

    def __start(self, update, context: CallbackContext):
        self.__ensure_private(update, context)

        if len(context.args) != 1:
            response = f"Usage: /start <user>"
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)
            return

        user_id = context.args[0]
        try:
            response = self._pharmacist.start(user_id)
        except PharmacistError as e:
            response = str(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    def __add_pill(self, update, context: CallbackContext):
        self.__ensure_private(update, context)
        try:
            pill = update.message.text
            response = self._pharmacist.add_pill(pill)
        except PharmacistError as e:
            response = str(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    def __cancel(self, update, context: CallbackContext):
        self.__ensure_private(update, context)
        try:
            response = self._pharmacist.cancel()
        except PharmacistError as e:
            response = str(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    def __ask(self, update, context: CallbackContext):
        self.__ensure_private(update, context)
        try:
            response = self._pharmacist.ask()
        except PharmacistError as e:
            response = str(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    def __ensure_private(self, update, context: CallbackContext):
        chat_id = update.effective_chat.id
        if chat_id not in self._allowed_chats:
            context.bot.send_message(chat_id=chat_id, text="This is a private bot. You cannot use it.")
            raise ValueError("Unauthorized user")

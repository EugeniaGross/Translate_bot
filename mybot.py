import logging
import os
import sys

from dotenv import load_dotenv
from googletrans import Translator
from telegram.ext import Filters, MessageHandler, Updater

from exceptions import BotError

load_dotenv()

token = os.getenv('TOKEN')

def check_tokens():
    if not token:
        return False
    return True

translator = Translator()


def translator_text_ru(update, context):
    """Перевод на английский язык."""
    logging.DEBUG('Начало перевода на английский язык')
    chat = update.effective_chat
    text = update.message.text
    result = translator.translate(text, dest='en')
    context.bot.send_message(chat_id=chat.id, text=result.text)


def translator_text_en(update, context):
    """Перевод на русский язык."""
    logging.DEBUG('Начало перевода на русский язык')
    chat = update.effective_chat
    text = update.message.text
    result = translator.translate(text, dest='ru')
    context.bot.send_message(chat_id=chat.id, text=result.text)


def main():
    if not check_tokens():
        logging.critical('Переменные окружения не доступны')
        sys.exit('Переменные окружения не доступны')
    try:
        updater = Updater(token)
        updater.dispatcher.add_handler(
            MessageHandler(
                Filters.regex('[А-Яа-яЁё]'),
                translator_text_ru
            )
        )
        updater.dispatcher.add_handler(
            MessageHandler(
                Filters.regex('[A-Za-z]'),
                translator_text_en
            )
        )
        updater.start_polling()
        updater.idle()
    except Exception as error:
        logging.error(f'Ошибка работы бота:{error}')
        raise BotError(f'Ошибка работы бота:{error}')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s, %(levelname)s, %(lineno)s, %(message)s, %(name)s',
    )
    main()

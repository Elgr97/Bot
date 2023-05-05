import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# Функция-обработчик сообщений
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f"Привет, {message.chat.username}! Я - бот, который поможет тебе конвертировать валюты. Напиши мне сообщение в формате: <из какой валюты> <в какую валюту> <сумма для конвертации>. Например: доллар рубль 100\n Для того, чтобы увидеть список доступных валют нажмите /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = f"Привет, {message.chat.username}! Для начала работы с ботом нажми /start"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

# Функция-обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    # Отправляем сообщение с результатом конвертации
    else:
        text = f'{amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)

# Запускаем телеграм-бота
bot.polling(none_stop=True)
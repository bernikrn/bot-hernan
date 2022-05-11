import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from random import randrange

TOKEN = "5272009742:AAGByVwgi_kF9Kvcao3bZkns9UF2ZP9X4_I"
# States
WELCOME, TOPICS, HISTORY, HISTORY2, CONTROL, WHERE, FUN, UP_FUN = range(8)

FUN_FACT_FILE = "fun_facts.txt"
HSM_IMAGE = "hsm.png"

bot_hsm = telegram.Bot(token=TOKEN)


def start(update: Update, context: CallbackContext) -> int:
    # bot.sendMessage(update.message.chat_id, "message123")
    bot_hsm.send_photo(update.message.chat_id, photo=open(HSM_IMAGE, 'rb'))
    reply_keyboard = [['/hola']]
    update.message.reply_text(
        'Hola soy el bot de Hernan\nDecime /hola para continuar',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Saludame'
        )
    ),
    # update.message.chat.id, photo = open(HSM_IMAGE, 'rb')
    # bot.send_photo(chat_id, photo=open('path', 'rb'))
    # update.message.photo(open('path', 'rb'))
    # send_photo("hsm2bot", open(HSM_IMAGE, 'rb'))
    return WELCOME


def topics(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['/control', '/historia', '/donde', '/fun_fact']]
    update.message.reply_text(
        'Podemos hablar sobre /control, /historia, /donde, /fun_fact',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=' '
        ),
    ),
    return TOPICS


def history(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['/mas_historia', '/inicio']]
    update.message.reply_text(
        'El laboratorio de Mecatronica comenzo como '
        'un club en el fondo de un aula. '
        'Queres saber /mas_historia o volver al menu anterior /inicio',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder=' '
        ),
    ),
    return HISTORY


def history2(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['/inicio']]
    update.message.reply_text(
        'Antes solo teniamos un dremel '
        'y un soldador de estaño. Volver al /inicio ',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='inicio'
        ),
    )
    return HISTORY2


def control(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['/inicio']]
    update.message.reply_text(
        'Yo no se mucho sobre teoria de control '
        'consulta al Hernan humano, el es especialista en control\n'
        'Volver a /inicio',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='inicio'
        ),
    )
    return CONTROL


def where(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['/inicio']]
    update.message.reply_text(
        'Hernan puede o no estar en el laboratorio '
        'en este momento. Volver a /inicio',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    ),
    return WHERE


def fun_fact(update: Update, context: CallbackContext) -> int:
    fun_facts_file = open(FUN_FACT_FILE, 'r')
    fun_facts_lines = fun_facts_file.readlines()
    update.message.reply_text(fun_facts_lines[randrange(len(fun_facts_lines))])
    fun_facts_file.close()
    update.message.reply_text('Quiero otro /fun_fact, volver a /inicio, o escribe tu propio fun fact ',
                              reply_markup=ReplyKeyboardRemove()
                              )
    return FUN


def up_fun_fact(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Gracias por subir tu fun fact, volver a /inicio, o escribe otro fun fact',
        reply_markup=ReplyKeyboardRemove()
    )
    fun_facts_file = open(FUN_FACT_FILE, 'a')
    fun_facts_file.write(update.message.text + '\n')
    fun_facts_file.close()
    return UP_FUN


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            'No entiendo que me estas diciendo. Habla con el Hernan humano\n'
            '/start para iniciar una conversacion'
            )
    )


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WELCOME: [CommandHandler('hola', topics)],
            TOPICS: [CommandHandler('historia', history),
                     CommandHandler('control', control),
                     CommandHandler('donde', where),
                     CommandHandler('fun_fact', fun_fact),
                     CommandHandler('start', start)],
            HISTORY: [CommandHandler('mas_historia', history2),
                      CommandHandler('inicio', topics)],
            HISTORY2: [CommandHandler('inicio', topics),
                       CommandHandler('inicio', topics)],
            CONTROL: [CommandHandler('start', start),
                      CommandHandler('inicio', topics)],
            WHERE: [CommandHandler('start', start),
                    CommandHandler('inicio', topics)],
            FUN: [CommandHandler('start', start),
                  CommandHandler('inicio', topics),
                  CommandHandler('fun_fact', fun_fact),
                  MessageHandler(Filters.text & ~Filters.command, up_fun_fact)],
            UP_FUN: [CommandHandler('inicio', topics),
                     MessageHandler(Filters.text & ~Filters.command, up_fun_fact)]},
        fallbacks=[CommandHandler('cancel', cancel)], )

    dispatcher.add_handler(conv_handler)
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

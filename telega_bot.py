import telebot
from states import Ordering


bot = telebot.TeleBot('token_here')
chats = {}


def check_user(message):
    global chats
    chat_id = message.chat.id
    if chat_id not in chats.keys():
        chats[chat_id] = Ordering(bot.send_message, chat_id)
    return chats[chat_id]

@bot.message_handler(commands=['order'])
def send_welcome(message):
    user_obj = check_user(message)
    user_obj.start()

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_obj = check_user(message)
    user_obj.get_message(message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
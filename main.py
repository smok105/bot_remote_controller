import telebot
import settings
import alsaaudio
from telebot import types
from selenium import webdriver

VOLUME = {'min': -10, 'max':10}
bot = telebot.TeleBot(settings.TOKEN)

def driver_sait(sait):
    chromedriver = "/home/dmitro/PycharmProjects/bot_01/chromedriver"
    driver = webdriver.Chrome(chromedriver)
    driver.get(str(sait))
    driver.find_element_by_id('button-header-play').click()


@bot.message_handler(commands=['start'])
def hello(message):
    sti = open('bot_image/hello',
               'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Добро пожаловать!\n"
                                     "<b>Я {1.first_name}</b>, создан для управлением компьютера Короля"
                                      .format(message.from_user,bot.get_me()),parse_mode='html')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=True,selective=True)
    item1 = types.KeyboardButton('/mixer')
    item2 = types.KeyboardButton('/music')
    item3 = types.KeyboardButton('/help')
    markup.add(item1, item2,item3)
    bot.send_message(message.chat.id, "В низу кнопки помогут тебе во всем разобраться ", reply_markup=markup)


@bot.message_handler(commands=['clear'])
def handler_clear(message):
    for id in range((message.message_id - 10), message.message_id):
        bot.delete_message(message.chat.id, id)


@bot.message_handler(commands=['mixer'])
def mixer(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Уменьшить кромкость(-10)',callback_data='min')
    item2 = types.InlineKeyboardButton('Увеличить громкость(+10)',callback_data='max')
    markup.add(item1,item2)
    bot.send_message(message.chat.id, 'Управление громкостью', reply_markup=markup)



@bot.message_handler(commands=['music'])
def music(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=True)
    item1 = types.KeyboardButton("Dex")
    item2 = types.KeyboardButton("Макс Корж")
    item3 = types.KeyboardButton("Eminem")
    item4 = types.KeyboardButton("Rammstein")
    markup.add(item1, item2,item3,item4)
    bot.send_message(message.chat.id, "Выбери артиста", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):

    if message.chat.type == 'private':
        if message.text == 'Dex':
            driver_sait('https://2muz.me/artist/dax')
            bot.send_message(message.chat.id, 'обрабатываю топ треки Dax')

        elif message.text == 'Макс Корж':
            driver_sait('https://2muz.me/artist/maks-korzh')
            bot.send_message(message.chat.id, 'обрабатываю топ треки Макс Корж')
        elif message.text == 'Eminem':
            driver_sait('https://2muz.me/artist/eminem')
            bot.send_message(message.chat.id, 'обрабатываю топ треки Eminem')
        elif message.text == 'Rammstein':
            driver_sait('https://2muz.me/artist/rammstein')
            bot.send_message(message.chat.id, 'обрабатываю топ треки Rammstein')


@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    if call.message:
        volume = VOLUME.get(call.data, 0)
        mix = alsaaudio.Mixer()
        volume_now = mix.getvolume()
        volume += volume_now[0]
        res = mix.getvolume()
        if 0 < volume < 100:
            mix.setvolume(volume)
            bot.send_message(call.message.chat.id, f'устнавлено занчение звука раное {res[0]}')
        else:
            bot.send_message(call.message.chat.id, f'превишенно значение задаваемого звука, сейчас равно {res[0]}')

bot.polling(none_stop=True)

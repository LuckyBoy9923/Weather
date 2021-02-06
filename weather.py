import requests
import telebot

url: str = 'http://api.openweathermap.org/data/2.5/weather'
api_weather = '1672f972ebc3d4a485ead6db03472d37'
api_telegram = '1517109563:AAFDTnX1bVta62Jp3uRo8lE3k0ttmRYp4FY'

bot = telebot.TeleBot(api_telegram)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Добро пожаловать, ' + str(message.from_user.first_name) + ',' + '\n' +
                     'чтоб узнать погоду напишите в чат название города｡◕‿ ◕｡')


@bot.message_handler(commands=['help'])
def welcome(message):
    bot.send_message(message.chat.id,
                     '/start запуск бота\n/help команды бота\nчтоб узнать погоду напишите в чат название города')


@bot.message_handler(content_types=['text'])
def test(message):
    city_name = message.text

    try:
        params = {'APPID': api_weather, 'q': city_name, 'units': 'metric', 'lang': 'ru'}
        result = requests.get(url, params=params)
        weather = result.json()

        if weather["main"]['temp'] < 5:
            status = "❄Сейчас холодно!"
        elif weather["main"]['temp'] < 15:
            status = "Сейчас прохладно!"
        elif weather["main"]['temp'] > 30:
            status = "☼Сейчас жарко!"
        else:
            status = "Сейчас отличная температура!"

        bot.send_message(message.chat.id, "В городе " + str(weather["name"]) + " температура: " + str(
            float(weather["main"]['temp']))+" ℃ " + "\n" +
                         "Максимальная температура: " + str(float(weather['main']['temp_max']))  + "℃"+ "\n" +
                         "Минимальная температура: " + str(float(weather['main']['temp_min']))  + "℃" + "\n" +
                         'Минимальная температура: ' + str( float( weather['main']['temp_min'] ) ) + "℃" + "\n" +
                         "☁Влажность: " + str(int(weather['main']['humidity']))  + "%" + "\n" +
                         "Описание: " + str(weather['weather'][0]["description"])  + "\n\n" + status)

    except:
        bot.send_message(message.chat.id, "Город " + city_name + " не найден☹")


if __name__ == '__main__':
    bot.polling(none_stop=True)

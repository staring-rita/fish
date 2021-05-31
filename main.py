#Импортировали библиотеку vk_api (pip install vka_pi)
from seting import VK_TOKEN, WEATHER_TOKEN
import vk_api
from vk_api import longpoll
#Дотсали из библиотеки две функции
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from settings import VK_TOKEN, WEATHER_TOKEN
#Переменная для хранения токена группы ВК
url = "http://api.openweathermap.org/data/2.5/weather"
api_key = WEATHER_TOKEN

keyboard = '{{"buttons":[[{"action":{"type":"text","label":"Москва","payload":""},"color":"negative"},{"action":{"type":"text","label":"Санкт-Петербург","payload":""},"color":"positive"},{"action":{"type":"text","label":"Улан-Удэ","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":"Новосибирск","payload":""},"color":"primary"},{"action":{"type":"text","label":"Кемерово","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":"Погода","payload":""},"color":"positive"}]]}""}]]}'

#Подключаем токен и longpoll
token_connection = vk_api.VkApi(token = token)
give = token_connection.get_api()
longpoll = VkLongPoll(token_connection)

def weather(city_name):
    params = {"APPID": api_key, "q": city_name, "units": "metric", "lang": "ru"}
    result = requests.get(url, params=params)
    weather = result.json()
    print(weather)
    result = ""
    if weather['cod'] == '404':
        result = "Город не найден"
    else:
        result = "В городе " + weather['name'] + '\n'
        result += "Погода: "+ weather['weather'][0]['description'] +"\n"
        result += "Температура " + str(weather['main']['temp']) + "°C\n"
        result += "Ощущается как " + str(weather['main']['feels_like']) + "°C\n"
        result += "Давление " + str(weather['main']['pressure']) + "ммрт\n"
        result += "Влажность " + str(weather['main']['humidity']) + "%\n"
        result += "Скорость ветра " + str(weather['wind']['speed']) + "м/с\n"
        result += "Восход " + str(weather['sys']['sunrise']) + "\n"
        result += "Закат " + str(weather['sys']['sunset']) + "\n"
    return result

#функция для ответа на сообщения в ЛС группы
def write_msg(id, text):
    token_connection.method('messages.send', {'user_id' : id, 'message' : text, 'random_id' : 0, "keyboard": keyboard})

#Функция формирования ответа бота
def answer(id, text):
    if text == 'привет' or text == 'начать':
        return 'Привет, я бот \n༼ つ ◕_◕ ༽つ\n👋\nЯ погодный бот'
    elif text == 'как дела?':
        return 'Хорошо, а как твои?'
    elif text == 'погода':
        write_msg(id, 'Напиши мне название города')
        #слушаем longpool и ждём новое сообщение боту
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                #если сообщение для бота
                if event.to_me:
                    #получаем текст сообщение и переводим его в нижний регистр
                    message = event.text.lower()
                    return weather(message) 
    else:
        return weather(text)

try:
    #слушаем longpool и ждём новое сообщение боту
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            #если сообщение для бота
            if event.to_me:
                #получаем текст сообщение и переводим его в нижний регистр
                message = event.text.lower()
                #получаем id пользователя
                id = event.user_id
                print("id:", id )
                text = answer(id, message)
                write_msg(id, text)
                print(id, message, event.datetime)

                user_get=give.users.get(user_ids = (id))
                print(user_get)
                first_name=user_get[0]['first_name']
                last_name=user_get[0]['last_name']
                full_name=first_name+" "+last_name
                print (full_name)
                

except KeyboardInterrupt:
    print("Stop")
finally:
    print()
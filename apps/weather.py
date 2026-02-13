import requests
import logging
import os
from dotenv import load_dotenv
from datetime import datetime

# Загружаем переменные из .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # api_ключ

CITY = "Kyiv"
COUNTRY = "UA"   # код страны Украины

def get_weather():

    # Функция, которая в зависимости от поля data[weather][0][main] - где: weather - это ключ словаря data, значение словаря
    # список, значит [0] - это первый элемент списка, а этот элемент тоже словарь, берем значения ключа main - там категория
    # погоды, возвращает эмодзи категории погоды
    def get_weather_emoji(main_weather):
        emoji_map = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Fog": "🌫️",
            "Haze": "🌫️",
            "Smoke": "🌫️",
            "Dust": "🌫️",
            "Sand": "🌫️",
            "Ash": "🌫️",
            "Squall": "🌬️",
            "Tornado": "🌪️"
    }
        return emoji_map.get(main_weather, "🌍")  # если неизвестно — нейтральный эмодзи

    # Базовый URL эндпоинта для текущей погоды
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    # Параметры запроса (query string) — передаём через params
    # Библиотека requests ожидает, что параметры запроса (те, которые пойдут в строку после ? в URL) будут переданы именно
    # в виде словаря, когда используется аргумент params=.
    params = {
        "q": f"{CITY},{COUNTRY}",      # город и страна
        "appid": API_KEY,              # обязательный ключ
        "units": "metric",             # метрическая система: °C, м/с, мм
        "lang": "uk"                   # язык описания погоды (можно "ru", "en")
    }

    try:
        # Делаем GET-запрос с параметрами
        response = requests.get(base_url, params = params, timeout = 10)

        # Проверяем, что запрос успешен
        response.raise_for_status()  # кинет исключение на 4xx/5xx

        # Парсим JSON
        data = response.json()

        weather_main = data['weather'][0]['main']

        # Подготавливаем сообщение
        emoji = get_weather_emoji(weather_main)
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        desc = data['weather'][0]['description'].capitalize()
        humidity = data['main']['humidity']
        wind_speed = data.get('wind', {}).get('speed', 0)   # если нет — 0 м/с

        # Формируем сообщение
        message = (
            f"{emoji} <b>Погода в {data['name']}</b> ({data['sys']['country']})\n\n"
            f"Температура: <b>{temp:.1f}°C</b>\n"
            f"Відчувається: <b>{feels_like:.1f}°C</b>\n"
            f"{desc}\n"
            f"Вологість: {humidity}%\n"
            f"Вітер: {wind_speed} м/с\n\n"
            f"<i>Оновлено: {datetime.now().strftime('%H:%M %d.%m.%Y')}</i>"
        )
        return message

    except Exception as e:
        logging.error(f"Помилка при отриманні погоди: {e}")
        return "Щось пішло не так... Спробуй пізніше ☹️"


import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Загружаем переменные из .env
load_dotenv()
API_KEY = os.getenv("EXCHANGERATES_API_KEY")  # api_ключ

def get_exchange_rates(currency):
    # Базовый URL эндпоинта
    base_url = "https://v6.exchangerate-api.com/v6/{key}/latest/{base}"

    try:
        url = base_url.format(key = API_KEY, base = currency)
        r = requests.get(url, timeout = 10)
        r.raise_for_status()    # кинет исключение на 4хх/5хх

        data = r.json()

        message = (
            f"💱 <b>Курс {currency} → UAH</b> :\n\n"
            f"1{currency} = {data['conversion_rates']['UAH']:.2f} грн.\n"
            f"<i>Оновлено: {datetime.now().strftime('%H:%M %d.%m.%Y')}</i>"
        )
        return message

    except requests.exceptions.RequestException as http_err:
        return f"HTTP-помилка {r.status_code}: {http_err}"

    except requests.exceptions.RequestException as req_err:
        return f"Проблема з мережею: {req_err}"

    except Exception as e:
        return f"Щось пішло не так: {e} ☹️"

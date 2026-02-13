import asyncio
import logging

import weather
import start_message
import exchange_rates

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv
import os

# Загружаем .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Глобальная главная клавиатура
MAIN_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Погода ☀️", callback_data="weather"),
        InlineKeyboardButton(text="Курс валют 💱", callback_data="exchange_menu")
    ],
    [
        InlineKeyboardButton(text="Цитата 💬", callback_data="quote"),
        # InlineKeyboardButton(text="Новини 📰", callback_data="news")
    ]
])


# Команда /start — приветствие + главное меню
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_name = message.from_user.first_name or "друг"
    text = start_message.get_start_message(user_name)

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=MAIN_KEYBOARD,
        disable_web_page_preview=True
    )


# Подменю "Курс валют"
@dp.callback_query(lambda c: c.data == "exchange_menu")
async def show_exchange_menu(callback: CallbackQuery):
    text = (
        "<b>💱 Курс валют</b>\n\n"
        "Обери базову валюту, щоб побачити курс до гривні:"
    )

    menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="USD 🇺🇸", callback_data="exchange_USD"),
            InlineKeyboardButton(text="EUR 🇪🇺", callback_data="exchange_EUR"),
        ],
        [
            InlineKeyboardButton(text="PLN 🇵🇱", callback_data="exchange_PLN"),
            InlineKeyboardButton(text="GBP 🇬🇧", callback_data="exchange_GBP"),
        ],
        [
            InlineKeyboardButton(text="KRW 🇰🇷", callback_data="exchange_KRW"),
            InlineKeyboardButton(text="CNH 🇨🇳", callback_data="exchange_CNH"),
        ],
        [
            InlineKeyboardButton(text="← Назад", callback_data="back_to_main")
        ]
    ])

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=menu)
    await callback.answer()


# Показ курса выбранной валюты
@dp.callback_query(lambda c: c.data.startswith("exchange_"))
async def show_currency_rate(callback: CallbackQuery):
    currency = callback.data.split("_")[1]  # exchange_USD → USD

    result_text = exchange_rates.get_exchange_rates(currency)

    back_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад до вибору валюти", callback_data="exchange_menu")]
    ])

    await callback.message.edit_text(result_text, parse_mode="HTML", reply_markup=back_button)
    await callback.answer(f"Курс {currency} завантажено!")


# Кнопка "Назад" к главному меню
@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    user_name = callback.from_user.first_name or "друг"
    text = start_message.get_start_message(user_name)

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=MAIN_KEYBOARD
    )
    await callback.answer()


# Обработчики остальных кнопок (погода, цитата и т.д.)
# Погода
@dp.callback_query(lambda c: c.data == "weather")
async def process_weather(callback: CallbackQuery):
    text = weather.get_weather()
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer("Погода завантажена!")

# Цитата (пока заглушка — потом заменишь)
@dp.callback_query(lambda c: c.data == "quote")
async def process_quote(callback: CallbackQuery):
    text = "Тут буде твоя цитата 😊 (поки що заглушка)"
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

# Новости (если добавишь позже)
@dp.callback_query(lambda c: c.data == "news")
async def process_news(callback: CallbackQuery):
    text = "Новини поки що не реалізовані 📰"
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()


# Команда /погода (на всякий случай, если кто-то напишет текстом)
@dp.message(Command("погода", "weather"))
async def weather_command(message: Message):
    text = weather.get_weather()
    await message.answer(text, parse_mode="HTML")


# Команда /курс (тоже на всякий случай)
@dp.message(Command("курс"))
async def exchange_rate_command(message: Message):
    args = message.text.split()
    currency = args[1].upper() if len(args) > 1 else 'USD'
    text = exchange_rates.get_exchange_rates(currency)
    await message.answer(text, parse_mode="HTML")


# Запуск
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
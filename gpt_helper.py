import openai
import os
from dotenv import load_dotenv
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_forecast(address, price, forecast_value, trend, inflation):
    user_prompt = f"""
Ты аналитик по недвижимости. Пользователь спрашивает про прогноз цены:
- Адрес: {address}
- Текущая цена: {price} ₽
- Прогноз на год: {forecast_value} ₽
- Изменение за последние 12 месяцев: {trend}
- Уровень инфляции в регионе: {inflation}%
Объясни, почему такая цена прогнозируется. Учитывай район, экономику, застройку, ипотеку. Кратко, понятно, до 250 слов.
"""

    messages = [
        {
            "role": "system",
            "content": (
                "Ты эксперт-аналитик по недвижимости. "
                "Объясняй кратко, уверенно и понятно. "
                "Не используй жаргон. Пиши объёмом до 250 слов."
            )
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    # Обработка ошибок и таймаутов
    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                timeout=20
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Ошибка GPT-подключения (попытка {attempt + 1}): {e}")
            time.sleep(2)

    return "Извините, не удалось получить объяснение от ИИ. Попробуйте позже."
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import openai
from predictor import make_forecast
from gpt_helper import explain_forecast

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Прогноз цен на недвижимость", layout="centered")

st.title("📈 Прогноз цен на недвижимость в России")
address = st.text_input("Введите адрес или район:")


# Фиктивные данные на 2 года
dates = pd.date_range(end=pd.Timestamp.today(), periods=730)
prices = [1000000 + i * 1000 for i in range(730)]  # линейный рост

df = pd.DataFrame({'ds': dates, 'y': prices})

if st.button("Показать прогноз"):
    if address:
        forecast, forecast_value, trend_str = make_forecast(df)
        current_price = df.iloc[-1]['y']

        st.line_chart(forecast.set_index("ds")["yhat"])
        st.success(f"💰 Прогнозируемая цена через год: {round(forecast_value)} ₽")

        explanation = explain_forecast(
            address=address,
            price=current_price,
            forecast_value=forecast_value,
            trend=trend_str,
            inflation=6.3
        )

        st.info(f"🤖 Объяснение: {explanation}")
    else:
        st.warning("Введите адрес для начала анализа.")
from prophet import Prophet
import pandas as pd

from prophet import Prophet
import pandas as pd

def forecast_price(address):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=730)
    prices = [1000000 + i * 1000 for i in range(730)]

    df = pd.DataFrame({'ds': dates, 'y': prices})

    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    price_in_year = forecast.iloc[-1]["yhat"]

    return forecast, price_in_year

def make_forecast(df, periods=365):
    """
    df — DataFrame с колонками: 'ds' (дата) и 'y' (цена)
    """
    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    # Прогнозируемое значение через 365 дней
    forecast_value = forecast.iloc[-1]['yhat']

    # Тренд: разница между сегодня и год назад
    last_12m = df[df['ds'] > (df['ds'].max() - pd.Timedelta(days=365))]
    if len(last_12m) >= 2:
        price_old = last_12m.iloc[0]['y']
        price_now = last_12m.iloc[-1]['y']
        trend_pct = ((price_now - price_old) / price_old) * 100
    else:
        trend_pct = 0

    # Приведение к читаемому виду
    trend_str = f"{'Рост' if trend_pct >= 0 else 'Падение'} на {abs(trend_pct):.1f}%"

    return forecast, forecast_value, trend_str
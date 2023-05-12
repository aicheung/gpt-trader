__all__ = ['get_stock_closing_prices', 'get_one_year_sliding_window_data', 'get_stock_prediction']

import yfinance as yf
import datetime
import openai

def get_stock_closing_prices(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return [(date.strftime('%Y-%m-%d'), row['Close']) for date, row in stock_data.iterrows()]

def get_one_month_sliding_window_data(ticker, base_date):
    base_date = datetime.datetime.strptime(base_date, '%Y-%m-%d')
    one_month_earlier = base_date - datetime.timedelta(days=30)
    start_date = one_month_earlier.strftime('%Y-%m-%d')
    end_date = (base_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    return get_stock_closing_prices(ticker, start_date, end_date)

def get_stock_prediction(sliding_window_data):
    # Format the sliding window data for input to the GPT model
    sliding_window_text = "\n".join([f"{date} {closing_price:.2f}" for date, closing_price in sliding_window_data])

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a stock prediction assistant that can analyze the past year's stock data and predict the next day's stock performance."},
            {"role": "user", "content": f"Here is the past year's daily closing prices for the stock:\n\n{sliding_window_text}\n\nPredict the stock performance for the next day. You should only output in the following format :predicted price-bullish or bearish-confidence(in percentages between 0 and 100)"}
        ]
    )

    return response.choices[0].message['content']

if __name__ == "__main__":
    ticker = input("Enter the stock symbol: ")
    base_date = input("Enter the base date (YYYY-MM-DD): ")

    sliding_window_data = get_one_month_sliding_window_data(ticker, base_date)
    prediction = get_stock_prediction(sliding_window_data)

    print("Prediction:", prediction)

import yfinance as yf
import datetime
import openai
import os
import pandas as pd
import pandas_market_calendars as mcal

from stock_sliding_window import get_stock_closing_prices, get_one_month_sliding_window_data, get_stock_prediction

def backtest_stock_prediction(ticker, start_date, end_date):
    # Get a calendar for the NYSE
    nyse = mcal.get_calendar('NYSE')

    # Get the valid trading days between the start and end dates
    valid_trading_days = nyse.valid_days(start_date=start_date, end_date=end_date)

    # Get the entire year's closing prices
    all_closing_prices = get_stock_closing_prices(ticker, start_date, end_date)
    all_closing_prices_dict = {date: closing_price for date, closing_price in all_closing_prices}

    errors = []
    total_predictions = 0

    for i, base_date in enumerate(valid_trading_days[:-1]):
        base_date_str = base_date.strftime('%Y-%m-%d')
        sliding_window_data = get_one_month_sliding_window_data(ticker, base_date_str)
        prediction = get_stock_prediction(sliding_window_data)

        try:
            predicted_price, _, _ = prediction.split("-")
            predicted_price = float(predicted_price)
        except ValueError:
            print(f"Failed to parse prediction for {base_date_str}: {prediction}")
            continue

        next_day = valid_trading_days[i + 1]
        next_day_str = next_day.strftime('%Y-%m-%d')

        if next_day_str in all_closing_prices_dict:
            actual_price = all_closing_prices_dict[next_day_str]
            error = abs(predicted_price - actual_price)
            errors.append(error)
            total_predictions += 1
            print(f"{base_date_str} - Actual: {actual_price:.2f}, Predicted: {predicted_price:.2f}, Error: {error:.2f}")
        else:
            print(f"No actual price found for {next_day_str}")

    mean_absolute_error = sum(errors) / total_predictions
    print(f"Mean Absolute Error: {mean_absolute_error:.2f}")

if __name__ == "__main__":
    ticker = input("Enter the stock symbol: ")
    end_date = datetime.date.today().strftime('%Y-%m-%d')
    start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')

    backtest_stock_prediction(ticker, start_date, end_date)

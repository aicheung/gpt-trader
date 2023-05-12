# GPT-Trader

GPT-Trader is an experimental project that uses GPT-4 to predict stock prices based on historical closing price data. This project is for educational purposes only and should not be used for real-world trading.

## Installation

1. Install the required Python packages from the `requirements.txt` file:
    ```
    pip install -r requirements.txt
    ```

2. Set up your OpenAI API key as an environment variable:
    ```
    export OPENAI_API_KEY=your_api_key_here
    ```

## Usage

1. Run the main script to interactively get a stock prediction for a specific date:
    ```
    python gpt-trader.py
    ```

2. Run the backtest script to evaluate the accuracy of GPT-4's predictions for a given date range:
    ```
    python backtest.py
    ```

## Disclaimer

This project is for educational purposes only and should not be used for real-world trading. The accuracy of GPT-4's stock predictions is not guaranteed and may lead to financial loss if used for trading.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

import time
import logging
from typing import Any, Dict

from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class TokenTrendRequest(Model):
    token : str


class TokenTrendResponse(Model):
    label : str


# Empty message class
class EmptyMessage(Model):
    pass


agent = Agent(
    name="Clustering Based Price Prediction",
    seed='Clustering Based Price Prediction',
    port=5051,
    endpoint=['http://localhost:5051/endpoint']
)

fund_agent_if_low(agent.wallet.address())

# async def get_trend(token):
#     your code to predict\
#     return label

import requests
import pandas as pd 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle
import time

pd.options.mode.chained_assignment = None
def fetch_historical_data(coin, days=30):
    """Fetch historical market data for a specific coin."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }
    
    for attempt in range(5):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            data = pd.DataFrame(response.json()['prices'], columns=['timestamp', 'price'])
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            return data  # Include today's data
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"Rate limit exceeded for {coin}. Retrying in {attempt + 1} seconds...")
                time.sleep(attempt + 1)
            else:
                print(f"Error fetching data for {coin}: {e}")
                return None
    return None

def calculate_features(data):
    """Calculate required features for prediction."""
    data['price_change'] = data['price'].diff()
    data['pct_change'] = data['price'].pct_change() * 100
    data['volatility'] = data['price'].rolling(window=3).std()  # 3-day volatility
    data['7_day_avg'] = data['price'].rolling(window=7).mean()  # 7-day moving average
    data['momentum'] = data['pct_change'].rolling(window=5).sum()  # 5-day momentum
    return data.dropna()

async def predict_trends_for_single_token(token):
    """Predict trends for a single token."""
    coin_id = token  # Use the token name as the coin ID

    try:
        # Load the KMeans model and scaler from .pkl files
        with open(f'kmeans_model_{coin_id}.pkl', 'rb') as model_file:
            kmeans_model = pickle.load(model_file)

        with open(f'scaler_{coin_id}.pkl', 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)
        logging.info(f"Scaler and Clustering Model Uploaded")
        # Fetch current day data for the coin
        current_data = fetch_historical_data(coin_id)

        if current_data is not None and not current_data.empty:
            # Use the last 7 days to calculate features
            features_data = calculate_features(current_data.iloc[-7:])  # Get the last 7 days

            # Prepare the features for the most recent day
            features_for_prediction = features_data[['price_change', 'pct_change', 'volatility', 'momentum', '7_day_avg']].iloc[-1:]

            # Scale the current features using the loaded scaler
            scaled_current_features = scaler.transform(features_for_prediction)

            # Predict the cluster using the KMeans model
            predicted_cluster = kmeans_model.predict(scaled_current_features)

            # Map predicted cluster to trend label
            trend_labels = {
                0: 'highly decrease',
                1: 'slightly decrease',
                2: 'neutral',
                3: 'slightly increase',
                4: 'highly increase'
            }
            predicted_trend = trend_labels[predicted_cluster[0]]
            return predicted_trend
        else:
            print(f"No data available for predicting trend for {coin_id.capitalize()}.")
            return "No data available"
    except Exception as e:
        print(f"An error occurred for {coin_id}: {e}")
        return "Error occurred"


@agent.on_rest_post("/rest/post", TokenTrendRequest, TokenTrendResponse)
async def handle_get(ctx: Context, req : TokenTrendRequest) -> Dict[str, Any]:
    ctx.logger.info("Received GET request")
    label = await predict_trends_for_single_token(req.token)
    ctx.logger.info(f"Sent the label {label}")
    return TokenTrendResponse(label=label)


if __name__ == "__main__":
    agent.run()

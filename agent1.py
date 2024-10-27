import time
from typing import Any, Dict
import praw
import re
import json
import nltk
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import defaultdict
import openai
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
    name="LLM Based Price Prediction",
    seed='LLM Based Price Prediction',
    port=5050,
    endpoint=['http://localhost:5050/endpoint']
)

fund_agent_if_low(agent.wallet.address())


async def predict_trends_from_tweets(token: str):
    # Load tweets from JSON file
    file_path='/Users/abhimanyugangani/Desktop/Hanooman/tweets.json'
    with open(file_path, 'r') as f:
        tweets = json.load(f)

    # Initialize VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    sentiments = []
    
    # Analyze sentiments of tweets
    for tweet in tweets:
        score = sia.polarity_scores(tweet['text'])
        sentiments.append({
            'text': tweet['text'],
            'compound': score['compound'],  # Use compound score for overall sentiment
            'currency': tweet.get('currency', 'unknown'),  # Use 'unknown' if currency is not specified
            'favorite_count': tweet.get('favorite_count', 0),  # Default to 0 if not specified
            'retweet_count': tweet.get('retweet_count', 0)  # Default to 0 if not specified
        })

    # Prepare a prompt based on sentiments
    prompt = "Based on the following sentiments from tweets:\n"
    for sentiment in sentiments:
        prompt += f"Tweet: {sentiment['text']}\n"
        prompt += f"Sentiment Score: {sentiment['compound']}\n"
        prompt += f"Currency: {sentiment['currency']}\n\n"
        prompt += f"so use this data "
        prompt += f"For the token {token} and make the prediction for it by reading the rules given forward"

    prompt += f"Provide a final trend classification for currency {token} based on the sentiment analysis, strictly only for strictly input{token} choosing from:\n"
    prompt += "Highly Increase, Slightly Increase, Neutral, Slightly Decrease, Highly Decrease. Also retuning value only has a string with any one element from [highly increase, slightly increase, neutral, slightly decrease, highly decrease]. strictly just only the elemnt in form of the list element. do not give brackets and inverted columns strictly just the element with all letters are small characters and case sensitive"

    # Call OpenAI GPT-3.5 for predictions
    openai.api_key = ('OPENAI_KEY')  # Use the provided API key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract predictions
    final_prediction = response['choices'][0]['message']['content'].strip()
    return final_prediction

@agent.on_rest_post("/rest/post", TokenTrendRequest, TokenTrendResponse)
async def handle_get(ctx: Context, req : TokenTrendRequest) -> Dict[str, Any]:
    ctx.logger.info("Received GET request")
    label=await predict_trends_from_tweets(req.token)
    ctx.logger.info(f"Sent the label {label}")
    return TokenTrendResponse(label=label)


if __name__ == "__main__":
    agent.run()

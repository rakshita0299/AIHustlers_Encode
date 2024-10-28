# AIHustlers_Encode

# Aim

To solve an Agent Track problem by creating a multi-agent cryptocurrency trend prediction system designed to leverage both statistical clustering and Large Language Models (LLMs) for comprehensive trend analysis. The project integrates two main agents: a trend analysis agent using K-means clustering for long-term predictions and an LLM-based agent that incorporates social media sentiment and interaction data.

# Overview

Trend Predictor Agent predicts trends for popular cryptocurrencies (Bitcoin, Ethereum, Goat, and Solana) using a multi-agent system. Each agent performs a specific role in analyzing long-term trends and social media sentiments, then communicates with each other to derive the final trend predictions. Social media analysis is useful for short-term predictions as the data is realtively a real time data. This collaborative approach aims to provide an accurate forecast of market behavior by combining machine learning and natural language processing (NLP) techniques. These agents communicate to a master agent using uagents library to provide its insights. Master agent is a langgraph agent which has a certain weighted ensembling algorithms for the prediction which gives us a final prediction.

# Methodology

# 1. Training an unsupervised learning model to predict trends of price change for tokens:

  Historical data from CoinGecko API for past day in periods of each minute is used upon an clustering algorithm to label them with it's trends which can be \[heavily decreasing, slightly decreasing, neutral, slightly increasing, heavily increasing\] and are stored in formats of Scaler and Clustering models.

# 2. Twitter Analysis
Using the twitter API following metrics are extracted for the releveant tickers for the tokens:

    "currency"
    "text"
    "creation_date"
    "favorite_count"
    "retweet_count"
    "reply_count"
    "quote_count"
    "views
    "user_follower_count"
    "user_following_count"
    "user_number_of_tweets"
    "is_verified"
    "is_blue_verified"
    "engagement_rate"
    "influence_score"

  These insightful data are then passed on to a JSON file.

# 3. LLM-Based Sentiment Agent with X datafeed (Agent-1)

The LLM-Based Sentiment and Interaction Agent is an agent created with the help of uagents library focusing on analyzing public sentiment and engagement metrics, which are integrated into the LLM model for enhanced market forecasting for short-term data periods. The model recieves the data from the json file created in step 2 feeded into GPT 3.5-turbo.
The model is provided with fine-tuned structured prompts for getting extracted features with improved accuracy and robustness before predicting trends. 
The insights are forwarded to the main agents.

# 4. Clustering Model Analysis Agent(Agent-2)

The Trend Analysis Agent is a uagent designed by fetch's technologies for long-term trend predictions. This agent:

Method: Utilizes the models created in step 2 to predict trends for current day data.

Trends: Defines and detects trends as:
Highly Increase
Slightly Increase
Neutral
Slightly Decrease
Highly Decrease

Cryptocurrencies Analyzed: Bitcoin, Ethereum, Goat, and Solana.

This agent’s clustering results are communicated with the main agent to inform predictions.

# 5. Main Agent (langgraph agent)
The two agents collaborate by sharing insights, enabling a unified prediction of trends. This system design enhances predictive capabilities by combining long-term statistical clustering with real-time social sentiment analysis. THe insights are transferred to this langgraph agent which uses a weighted algorithm to predict a common predicted trends from long term and short term prediction at real-time.

# Architecture

![Alt text]([path/to/your/image.png](https://github.com/rakshita0299/AIHustlers_Encode/blob/main/Architecture.drawio.png))


# Data Sources

Twitter API: For engagement metrics, follower count, and other social signals.
CoinGecko : For generating hisctorical and current data for the clustering model's training and testing.

# Python Files

agent1.py -> LLM based sentiment agent
agent2.py -> Clustering Model Analysis agent
lang.py -> Main agent

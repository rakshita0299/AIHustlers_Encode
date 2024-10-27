# AIHustlers_Encode

# Agent Track

Agent Track is a multi-agent cryptocurrency trend prediction system designed to leverage both statistical clustering and Large Language Models (LLMs) for comprehensive trend analysis. The project integrates two main agents: a trend analysis agent using K-means clustering for long-term predictions and an LLM-based agent that incorporates social media sentiment and interaction data.

# Overview

Agent Track predicts trends for popular cryptocurrencies (Bitcoin, Ethereum, Goat, and Solana) using a multi-agent system. Each agent performs a specific role in analyzing long-term trends and social media sentiments, then communicates with each other to derive the final trend predictions. Social media analysis is useful for short-term predictions as the data is realtively a real time data. This collaborative approach aims to provide an accurate forecast of market behavior by combining machine learning and natural language processing (NLP) techniques.

# Agents and Methodology

# 1. Trend Analysis Agent

The Trend Analysis Agent is designed for long-term trend predictions. This agent:

Method: Utilizes the K-means clustering algorithm to group historical market data (5 days ago) into trend categories. To test the trend prediction the current day trend is predicted.

Trends: Defines and detects trends as:
Highly Increase
Slightly Increase
Neutral
Slightly Decrease
Highly Decrease

Cryptocurrencies Analyzed: Bitcoin, Ethereum, Goat, and Solana.

This agent’s clustering results are communicated with the second agent to inform predictions.

# 2. LLM-Based Sentiment and Interaction Agent

The LLM-Based Sentiment and Interaction Agent focuses on analyzing public sentiment and engagement metrics, which are integrated into the LLM model for enhanced market forecasting.

# Reddit Analysis

Sentiment Analysis: Extracts sentiment (positive, negative, neutral, and compound) from Reddit posts.
Interaction Analysis: Calculates engagement weight by summing upvotes and comments, indicating a post's influence on market perception.

# Twitter Analysis

Metrics: Retrieves engagement rate, follower count, and other relevant indicators from Twitter using the Twitter API.
Feature Extraction: Processes these social metrics for integration into the LLM model.

The model is fine-tuned with structured prompts and the extracted features to improve accuracy before predicting trends.

# Multi-Agent Communication

The two agents collaborate by sharing insights, enabling a unified prediction of trends. This system design enhances predictive capabilities by combining long-term statistical clustering with real-time social sentiment analysis.

# Data Sources

Reddit API: For sentiment and interaction data.

Twitter API: For engagement metrics, follower count, and other social signals.

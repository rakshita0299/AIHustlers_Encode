import os
import requests
import json
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, FunctionMessage
from typing import TypedDict, Sequence, Union, Annotated
import operator
import math

# Define custom tools

# Tool 1 - Trend Prediction with News & Reddit Impressions
def post_token_price_trend(token: str):
    url = "http://localhost:5051/rest/post"
    headers = {"Content-Type": "application/json"}
    data = {"token": token}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Tool 2 - Clustering for Trend Analysis
def post_token_clustering(token: str):
    url = "http://localhost:5050/rest/post"
    headers = {"Content-Type": "application/json"}
    data = {"token": token}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Define the agent's state
class AgentState(TypedDict):
    coin: str
    trend_prediction: dict
    trend_clustering: dict
    final_trend: Union[str, None]

def interpret_trend(state):    

    trend_prediction = state['trend_prediction']
    trend_clustering = state['trend_clustering']
    # Define weights for each source of prediction
    weights = {
        'prediction': 0.5,  # Weight for trend prediction
        'clustering': 0.5    # Weight for trend clustering
    }

    # Get the labels from the predictions
    prediction_label = trend_prediction.get('label')
    clustering_label = trend_clustering.get('label')

    # Define a mapping of labels to numerical values for weighted calculations
    label_to_value = {
        'highly increase': 1,
        'slightly increase': 0.5,
        'neutral': 0,
        'slightly decrease': -0.5,
        'highly decrease': -1
    }

    # Convert labels to numerical values based on the mapping
    prediction_value = label_to_value.get(prediction_label, 2)  # Default to Neutral if not found
    clustering_value = label_to_value.get(clustering_label, 2)  # Default to Neutral if not found

    # Calculate weighted average
    combined_value = (weights['prediction'] * prediction_value + weights['clustering'] * clustering_value)
    
    final_value = math.ceil(combined_value)

    value_to_trend = {
        1: 'highly increase',
        0.5: 'slightly increase',  # Added for better granularity
        0: 'neutral',
        -0.5: 'slightly decrease',  # Added for better granularity
        -1: 'highly decrease',  # Added for better granularity
    }

    # Get the final trend based on the ceiling value
    final_trend = value_to_trend.get(final_value, 'highly increase') #default value of highly increase if ceil value goes out of range

    return {'final_trend': final_trend}

# Set up the LangGraph
graph = StateGraph(AgentState)

# Define nodes with unique names
graph.add_node("get_coin", lambda state: {"coin": state['coin']})
graph.add_node("analyze_trend_prediction", lambda state: {"trend_prediction": post_token_price_trend(state['coin'])})
graph.add_node("analyze_trend_clustering", lambda state: {"trend_clustering": post_token_clustering(state['coin'])})
graph.add_node("determine_final_trend", interpret_trend)

# Define edges
graph.set_entry_point("get_coin")
graph.add_edge("get_coin", "analyze_trend_prediction")
graph.add_edge("analyze_trend_prediction", "analyze_trend_clustering")
graph.add_edge("analyze_trend_clustering", "determine_final_trend")
graph.set_finish_point("determine_final_trend")

# Compile the graph
app = graph.compile()

# Prompt the user for the coin name and pass it to the graph
user_coin = input("Enter the coin name (e.g., ethereum, bitcoin, solana, goatseus_maximus): ")
user_input = {"coin": user_coin}

# Invoke the graph with the user-provided coin name
result = app.invoke(user_input)
print("Final Trend Classification:", result['final_trend'])

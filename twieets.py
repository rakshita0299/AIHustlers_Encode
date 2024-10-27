import requests
import time
from json import dumps

# Your RapidAPI key
rapidapi_key = "RAPID_API_KEY"


# Function to fetch tweets based on cryptocurrency symbols
def fetch_tweets_for_symbols(symbols, min_retweets=1, min_likes=1, limit=5, start_date="2022-01-01"):
    base_url = "https://twitter154.p.rapidapi.com/search/search"
    headers = {
        "x-rapidapi-host": "twitter154.p.rapidapi.com",
        "x-rapidapi-key": rapidapi_key
    }

    # List to store tweet data
    tweets_data = []

    # Loop through each symbol in the list of symbols
    for symbol in symbols:
        params = {
            "query": f"#{symbol}",
            "section": "top",
            "min_retweets": min_retweets,
            "min_likes": min_likes,
            "limit": limit,
            "start_date": start_date,
            "language": "en"
        }

        # Make a request to fetch tweets for each symbol
        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()

        # Collect relevant data for each tweet in the response
        for tweet in data.get("results", []):
            tweet_info = {
                "currency": symbol,
                "text": tweet.get("text"),
                "creation_date": tweet.get("creation_date"),
                "favorite_count": tweet.get("favorite_count"),
                "retweet_count": tweet.get("retweet_count"),
                "reply_count": tweet.get("reply_count"),
                "quote_count": tweet.get("quote_count"),
                "views": tweet.get("views"),
                "user_follower_count": tweet["user"].get("follower_count"),
                "user_following_count": tweet["user"].get("following_count"),
                "user_number_of_tweets": tweet["user"].get("number_of_tweets"),
                "is_verified": tweet["user"].get("is_verified"),
                "is_blue_verified": tweet["user"].get("is_blue_verified")
            }

            # Calculate engagement rate if views are available
            if tweet_info["views"]:
                tweet_info["engagement_rate"] = (
                                                        (tweet_info["favorite_count"] or 0) +
                                                        (tweet_info["retweet_count"] or 0) +
                                                        (tweet_info["reply_count"] or 0)
                                                ) / tweet_info["views"]

            # Calculate influence score if following count is non-zero
            if tweet_info["user_following_count"]:
                tweet_info["influence_score"] = tweet_info["user_follower_count"] / tweet_info["user_following_count"]

            # Add the processed tweet data to the list
            tweets_data.append(tweet_info)

        # Rate limiting: Wait between requests
        time.sleep(0.2)
        print(len(tweets_data))

    # Return collected tweets data as JSON string
    print(len(tweets_data))
    return dumps(tweets_data, indent=2)


# Example usage with symbols for cryptocurrency
symbols = ["$BTC", "$ETH", "$SOL", "$GOAT"]
tweets_json = fetch_tweets_for_symbols(symbols, min_retweets=5, min_likes=10, limit=50, start_date="2024-10-25")
print(tweets_json)

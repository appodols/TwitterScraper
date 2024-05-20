import requests
import pandas as pd
import argparse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def fetch_tweets(user_id, cursor=None):
    api_key = os.getenv("API_KEY")
    url = f"https://api.socialdata.tools/twitter/user/{user_id}/tweets-and-replies"
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    params = {"cursor": cursor}

    # Print the request details
    print("Request URL:", url)
    print("Request Headers:", headers)
    print("Request Parameters:", params)

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data:", response.status_code, response.text)
        return None


def process_tweet(json_data):
    return {
        "tweet_created_at": json_data.get("tweet_created_at"),
        "id": json_data.get("id_str"),
        "full_text": json_data.get("full_text"),
        "source": json_data.get("source"),
        "user_name": json_data["user"].get("name"),
        "user_screen_name": json_data["user"].get("screen_name"),
        "followers_count": json_data["user"].get("followers_count"),
        "retweet_count": json_data.get("retweet_count"),
        "favorite_count": json_data.get("favorite_count"),
        "lang": json_data.get("lang"),
        "views_count": json_data.get("views_count"),
        "bookmark_count": json_data.get("bookmark_count"),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch tweets and save to CSV.")
    parser.add_argument("user_id", type=str, help="The user ID to fetch tweets for")

    args = parser.parse_args()
    user_id = args.user_id
    cursor = None
    all_tweets = []

    while True:
        data = fetch_tweets(user_id, cursor)

        if data:
            tweets = data.get("tweets", [])
            all_tweets.extend([process_tweet(tweet) for tweet in tweets])

            cursor = data.get("next_cursor")
            if not cursor:
                break
        else:
            break

    df = pd.DataFrame(all_tweets)
    df.to_csv("twitter_data.csv", index=False)
    print("Data saved to twitter_data.csv")


if __name__ == "__main__":
    main()

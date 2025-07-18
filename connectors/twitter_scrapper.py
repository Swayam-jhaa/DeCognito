import tweepy

def scrape_twitter(username):
    try:
        bearer_token = "AAAAAAAAAAAAAAAAAAAAAOwp3AEAAAAAvicR4BjNfAmLGttFdGU4qEBFsb4%3DSMQtKgAit99ZAx66GsG850XStmFbE9BwNifmqsyXRQ7N9CFCq2"
        client = tweepy.Client(bearer_token=bearer_token)
        user = client.get_user(username=username)
        tweets = client.get_users_tweets(id=user.data.id, max_results=5)
        tweet_list = []
        for tweet in tweets.data:
            content = tweet.text[:100]
            tweet_list.append({"content": content})
        return {"username": username, "tweets": tweet_list}
    except Exception as e:
        return {"error": str(e)}
# Reddit Sentiment Tradding Bot

### Parameters
```python
sentimentList = []
neededSentiments = 300
TRADE_SYMBOL = "BTCUSDT"
TRADE_QUANTITY = 0.001
in_position = "False"
```
### Reddit Client
```python
reddit = praw.Reddit(
    client_id=config.REDDIT_ID,
    client_secret=config.REDDIT_SECRET,
    password=config.REDDIT_PASS,
    user_agent="USERAGENT",
    username=config.REDDIT_USER,
)
```
### Binance Client
```python
client = Client(config.BINANCE_KEY, config.BINANCE_SECRET)
```

A simple but not efficient bot because textblob method is not perfect to find the sentiment of sentence.
```
By Muhammad Hanan Asghar
```

"""
Praw is a package to interface with reddit and subreddits.
"""
import praw
import config
import string
from textblob import Word
from textblob import TextBlob
from binance.client import Client
from binance.enums import ORDER_TYPE_MARKET
from binance.enums import SIDE_BUY
from binance.enums import SIDE_SELL

# Binance Instance
client = Client(config.BINANCE_KEY, config.BINANCE_SECRET)

# Reddit Instance
reddit = praw.Reddit(
    client_id=config.REDDIT_ID,
    client_secret=config.REDDIT_SECRET,
    password=config.REDDIT_PASS,
    user_agent="USERAGENT",
    username=config.REDDIT_USER,
)
# Stopwords
stop_words = ['get', 'us', 'see', 'use', 'said', 'asked', 'day', 'go', 'even', 'ive', 'right', 'left', 'always',
              'would',
              'told', 'would', 'one', 'ive', 'also', 'ever', 'x', 'take', 'let']

# Variables
sentimentList = []
neededSentiments = 300
TRADE_SYMBOL = "BTCUSDT"
TRADE_QUANTITY = 0.001
in_position = "False"


# Function that cleans the text
def cleaner(line):
    """
    :param line: text line
    :return: cleaned line
    """
    line = line.lower()
    line = line.strip()
    table = str.maketrans('', '', string.punctuation + string.digits + '”' + "’" + '“')
    words = line.split()
    stripped = [w.translate(table) for w in words]
    stp_words_rm = [word for word in stripped if word not in stop_words]
    cln_words = [Word(word).lemmatize() for word in stp_words_rm]
    line = " ".join(cln_words)
    line = line.replace("  ", " ")
    line = line.replace("  ", " ")
    return line


# Function that performs orders
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending Order....")
        _order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("Error Occurred during Execution of Order " + e)
        return False
    return True


# Getting Average
def Average(sentimentlst: list):
    sentimentlst = sentimentlst[-neededSentiments:]
    return sum(sentimentlst) / neededSentiments


for comment in reddit.subreddit("bitcoin").stream.comments():
    cleaned_line = cleaner(comment.body)
    blob = TextBlob(cleaned_line)
    if blob.sentiment.polarity != 0.0:
        sentimentList.append(blob.sentiment.polarity)
        if len(sentimentList) > 300:
            if round(Average(sentimentlst=sentimentList)) > 0.5:
                print("BUY.")
                if in_position:
                    print("Already Bought the Stock.")
                else:
                    order_success = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_success:
                        in_position = True
                        print("Stock has Bought.")
            elif round(Average(sentimentlst=sentimentList)) < -0.5:
                print("SELL")
                if in_position:
                    order_success = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_success:
                        in_position = False
                        print("Stock has Sold.")

        else:
            print(f"{len(sentimentList)} Less than 300.")

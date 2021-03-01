import re, tweepy, datetime, time, json, csv
from tweepy import OAuthHandler
 
#It will fetch all the tweets from current date till the startDate 
startDate = datetime.datetime(2020, 1, 1, 0, 0, 0)
endDate = datetime.datetime(2020,12,1,0,0,0)

# keys and tokens from my Twitter Dev Console
access_token="1286978390684102656-oWZlF2HOSfABnpTljM4XB6efndVoYv"
access_token_secret="hyycDQAK5rvMup7qw4HQvPVo4ZY6BUiF8jSR1ppmWWJQa"
consumer_key="VH9cMzWhLS6zHTIQ7V8g0WuJw"
consumer_secret="l3eWhWIjQnH82MMY0M3tmLofHqHqBvEGCH1I7PdNc83cqdhRgX"


# attempt authentication
try:
    # create OAuthHandler object
    auth = OAuthHandler(consumer_key, consumer_secret)
    # set access token and secret
    auth.set_access_token(access_token, access_token_secret)
    # create tweepy API object to fetch tweets
    api = tweepy.API(auth, wait_on_rate_limit=True)
    #data = self.api.rate_limit_status()
    print("Authentication Successfull")
except:
    print("Error: Authentication Failed")

 
def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return str(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()))


def get_tweets(query, count, start):
    '''
    Main function to fetch tweets and parse them.
    '''
    # empty list to store tweets
    tweets = []
    # call twitter api to fetch tweets

    #Creates a text-file and appends all the cleaned tweets
    with open('Output.csv', 'a', encoding="utf8", newline='') as the_file:
        fieldnames = ['text', 'date', 'number_of_retweet']
        writer = csv.DictWriter(the_file, fieldnames=fieldnames)
        writer.writerow({'text':'text', 'date':'date', 'number_of_retweet':'retweet_count'})

        print("Fetching tweets.........")

        for tweet in tweepy.Cursor(api.search, q=query, lang="en").items(count):
            if tweet.created_at > startDate and tweet.created_at < endDate:
                cleaned_tweet = clean_tweet(tweet.text)
                if cleaned_tweet not in tweets:
                    tweets.append(cleaned_tweet)
                    writer.writerow({'text':cleaned_tweet, 'date':tweet.created_at, 'number_of_retweet':tweet.retweet_count})

    the_file.close()

    # returns the list of tweets
    return tweets
 
#Calls the function by specifing keyword, number of tweets to be parsed from API and start date
Tweets = get_tweets(query = '$AMZN',count=20000, start=startDate)
print("Number of tweets fetched = ", len(Tweets))
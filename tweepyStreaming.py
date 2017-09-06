#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

#Variables that contains the user credentials to access Twitter API 
access_token = "*****************************"
access_token_secret = "*********************************"
consumer_key = "*****************************************"
consumer_secret = "*******************************************"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.num_tweets = 0
    def on_data(self, data):
        print(data)
        data = json.loads(data)
        if 'lang' in data and data['lang'] == 'en' and ('trump' in data['text'] or 'Trump' in data['text']) and self.num_tweets < 6:
            print('english trump tweet received ', data['text'])
            self.num_tweets += 1
            with open('NorthTweets.json', 'a') as file:
                file.write(data)
            return True
        elif self.num_tweets > 5 :
            return False
    def on_error(self, status):
        print 'error ', status
if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['Trump'])
    
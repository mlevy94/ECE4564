# import statements
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from sockcomm import SockClient  # import socket client
from md5auth import createMD5, authMD5  # import md5

import json

# the different api keys that were used from
ConsumerKey = '59wpwT8H9aBOXwljguKDa4Y6f'
ConsumerSec = 'JUF8xZ6oewvtYn20jAP3Sn6WSQJN7VClGSCOjGLCffUKUfcVcR'
AccessToken = '830234802766888964-iuUW1EamZqfZdB6lYPAipYU7Pxi50Bt'
AccessSecret = 'xZbenKmotSmxd1tqHzZlkQQctIne9t4p1p2sp1BjOuVTa'


# creation of the Streamlistener object.
# Code derived from https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/

class SListener(StreamListener):
    client = None

    # the definition of what to do on data associated with our account
    def on_data(self, data):

        data = json.loads(data)  # load data into json format
        if data["user"]["id"] == 830234802766888964:  # if the data originated from our
            # account ignore it. stops repeated data
            return True

        screenname = data["user"]["screen_name"]  # load data for later use
        tweetid = data["id"]
        tweet = data["text"]

        address = tweet.split("@4564Team_13 ##")[1].split(":")[0]  # split the tweet into different information
        port = tweet.split(":")[1].split("_")[0]
        question = [tweet.split('_"')[1].split('"')[0]]
        client = None
        if self.client is not None:  # setting up the client
            ip = self.client.getIP()
            if ip != (address, int(port)):
                self.client = SockClient(addr=address, port=int(port))
        else:
            self.client = SockClient(addr=address, port=int(port))

        md5 = createMD5(question)  # using the md5 to create the question package
        self.client.send((md5, question))

        recvMD5, answers = self.client.recv()[1]  # receiving the md5 and post to answer
        if not authMD5(recvMD5, answers):
            raise Exception("Bad MD5")
        for answer in answers:
            totalanswer = '@{} Team_13 "{}"'.format(screenname, answer)  # post answer to twitter
            if len(totalanswer) >= 140:  # if anwser is longer than 140 characters, truncate
                totalanswer = totalanswer[:137] + '...'
                api.update_status(totalanswer)

            else:
                api.update_status(totalanswer)

        return True

    def on_error(self, status):
        print(status)


# authorizing the API and creating the stream
auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSec)
auth.set_access_token(AccessToken, AccessSecret)
api = tweepy.API(auth)

twitterStream = Stream(auth, SListener())

twitterStream.filter(follow=['830234802766888964'])

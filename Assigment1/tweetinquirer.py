import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from sockcomm import SockClient

import json

ConsumerKey = '59wpwT8H9aBOXwljguKDa4Y6f'
ConsumerSec = 'JUF8xZ6oewvtYn20jAP3Sn6WSQJN7VClGSCOjGLCffUKUfcVcR'
AccessToken = '830234802766888964-iuUW1EamZqfZdB6lYPAipYU7Pxi50Bt'
AccessSecret = 'xZbenKmotSmxd1tqHzZlkQQctIne9t4p1p2sp1BjOuVTa'


class SListener(StreamListener):

    client = None

    def on_data(self,data):


        data = json.loads(data)
        if data["user"]["id"] == 830234802766888964:
            return True

        screenname = data["user"]["screen_name"]
        tweetid = data["id"]
        tweet = data["text"]


        address = tweet.split("@4564Team_13 ##")[1].split(":")[0]
        port = tweet.split(":")[1].split("_")[0]
        question = tweet.split('_"')[1].split('"')[0]

        if self.client is not None:
            ip = self.client.getIP()
            if ip != (address, int(port)):
                self.client = SockClient(addr=address, port=int(port))
        else:
            self.client = SockClient(addr=address, port=int(port))

        md5 = None
        self.client.send((md5,question))

        recvMD5, answers = self.client.recv()[1]
        #verify md5
        for answer in answers:
            totalanswer = '@{} Team_13"{}"'.format(screenname, answer)
            if len(totalanswer) >= 140:
                totalanswer = totalanswer[:137] + '...'
                api.update_status(totalanswer)

            else:
                api.update_status(totalanswer)



        return True

    def on_error(self,status):
        print(status)


auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSec)
auth.set_access_token(AccessToken, AccessSecret)
api = tweepy.API(auth)

twitterStream = Stream(auth, SListener())

twitterStream.filter(follow=['830234802766888964'])






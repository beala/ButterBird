import twitter
import time
import bbconfig

from _continuation import continulet

def wrap_api(api):
    def wrap_call(api_call, *args, **kwargs):
        while api.GetRateLimitStatus()["remaining_hits"] < 10:
            sleep(10 * 60)
        return api_call(*args, **kwargs)
    return wrap_call

class Tweeter(object):
    """This class posts to the main account"""

    def __init__(self, retreiver, post_interval, test_mode=False):
        """
           post_interval = Min number of seconds between updates.
        """
        self.retriever = retreiver
        self.post_interval = post_interval
        self.test_mode = test_mode
        self.api = twitter.Api(
                consumer_secret=bbconfig.consumer_sec,
                consumer_key=bbconfig.consumer_key,
                access_token_key=bbconfig.access_key,
                access_token_secret=bbconfig.access_sec)
        self.api.VerifyCredentials()
        self.apiCaller = wrap_api(self.api)

    def run(self, cont):
        while True:
            while not (9 <= time.localtime().tm_hour < 22):
                time.sleep(60 * 5)
            tweet = self.retriever.switch()
            self.post_update(tweet)
            time.sleep(self.post_interval)

    def post_update(self, tweet):
        if self.test_mode:
            print "Test tweet: " + tweet.text
        else:
            pass
            #self.apiCaller(self.api.PostUpdate, tweet.text)

class Retriever(object):
    """This class retrieves and deletes from the queue account."""

    def __init__(self, retrieve_interval, test_mode=False):
        self.retrieve_interval = retrieve_interval
        self.api = twitter.Api(
                consumer_secret=bbconfig.consumer_sec,
                consumer_key=bbconfig.consumer_key,
                access_token_key=bbconfig.ret_access_key,
                access_token_secret=bbconfig.ret_access_sec)
        self.api.VerifyCredentials()
        self.apiCaller = wrap_api(self.api)

    def retrieveTweet(self, cont):
        while True:
            timeline = self.getTimeline()
            while len(timeline) == 0:
                time.sleep(self.retrieve_interval)
                timeline = self.getTimeline()
            tweet = timeline[-1]
            cont.switch(tweet)
            #self.apiCaller(self.api.DestroyStatus(tweet.id))

    def getTimeline(self):
        return self.apiCaller(self.api.GetUserTimeline)

retriever_cont = continulet(Retriever(5*60, True).retrieveTweet)
tweeter_cont = continulet(Tweeter(retriever_cont, bbconfig.check_interval, True).run)

tweeter_cont.switch()

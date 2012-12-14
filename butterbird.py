import twitter
import time
import bbconfig

def wrap_api(api):
    """Wraps calls to the Twitter API, and checks how many hits are remaining.
       Backs off exponentially if there are < 10 hits.
       ((*args, **kwargs) => *) => (*args, *kwargs) => *
    """
    def wrap_call(api_call, *args, **kwargs):
        backoff = 5
        while api.GetRateLimitStatus()["remaining_hits"] < 10:
            sleep(backoff * 60)
            backoff *= 2
        return api_call(*args, **kwargs)
    return wrap_call

class Tweeter(object):
    """This class posts to the main account"""

    def __init__(self, twitter_api, retreiver, post_interval, test_mode=False):
        """
           retriever: Retriever.retrieve_tweet continulet.
           post_interval = Min number of seconds between updates.
           test_mode: if True, statuses aren't posted, just echo'd.
        """
        self.retriever = retreiver
        self.post_interval = post_interval
        self.test_mode = test_mode
        self.api = twitter_api
        self.api.VerifyCredentials()
        self.apiCaller = wrap_api(self.api)

    def timeToTweet(self):
        """() => Boolean"""
        return (9 <= time.localtime().tm_hour < 22)

    def run(self):
        """Get a tweet from the queue, post it to the main account.
           () => None
        """
        while True:
            while not self.timeToTweet():
                # Sleep at night.
                time.sleep(60 * 5)
            tweet, succCallback = self.retriever.next()
            # Need to test again in case retriever has been spinning all night.
            if self.timeToTweet():
                self.post_update(tweet)
                succCallback()
                time.sleep(self.post_interval)

    def post_update(self, tweet):
        """(String) => None"""
        if self.test_mode:
            print "Test tweet: " + tweet.text
        else:
            self.apiCaller(self.api.PostUpdate, tweet.text)
            print "Tweet: " + tweet.text

class Retriever(object):
    """This class retrieves and deletes from the queue account."""

    def __init__(self, twitter_api, retrieve_interval, test_mode=False):
        self.retrieve_interval = retrieve_interval
        self.test_mode = test_mode
        self.api = twitter_api
        self.api.VerifyCredentials()
        self.apiCaller = wrap_api(self.api)

    def retrieve_tweet(self):
        """Generator that returns a tweet from the queue account and a callback
           which deletes the tweet. Spins until a tweet has been retrieved.
           () => String, (() => *)
        """
        while True:
            timeline = self.get_timeline()
            while len(timeline) == 0:
                time.sleep(self.retrieve_interval)
                timeline = self.get_timeline()
            tweet = timeline[-1]
            if not self.test_mode:
                succCallback = lambda : self.apiCaller(self.api.DestroyStatus, tweet.id)
            else:
                succCallback = lambda : None
            yield tweet, succCallback

    def get_timeline(self):
        """() => List[Tweets]
        """
        return self.apiCaller(self.api.GetUserTimeline)

if __name__ == "__main__":
    tweeter_api = twitter.Api(
            consumer_secret=bbconfig.consumer_sec,
            consumer_key=bbconfig.consumer_key,
            access_token_key=bbconfig.access_key,
            access_token_secret=bbconfig.access_sec)
    retriever_api = twitter.Api(
            consumer_secret=bbconfig.consumer_sec,
            consumer_key=bbconfig.consumer_key,
            access_token_key=bbconfig.ret_access_key,
            access_token_secret=bbconfig.ret_access_sec)
    retriever_cont = Retriever(retriever_api, bbconfig.check_interval, bbconfig.test_mode).retrieve_tweet()
    Tweeter(tweeter_api, retriever_cont, bbconfig.tweet_interval, bbconfig.test_mode).run()

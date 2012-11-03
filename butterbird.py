import twitter
import time
import sys
import bbconfig

api = twitter.Api(
        consumer_secret=bbconfig.consumer_sec,
        consumer_key=bbconfig.consumer_key,
        access_token_key=bbconfig.access_key,
        access_token_secret=bbconfig.access_sec)

api.VerifyCredentials()

def UpateDummy(text):
    print "Dummy update: " + text

if bbconfig.test_mode == True:
    api.PostUpdate = UpateDummy

## Ask user what tweet to start with.
# Get the most recent tweets and print them.
recent_updates = api.GetUserTimeline(bbconfig.queue_username)
for num, update in enumerate(recent_updates[:-1]):
    print "%d. %s [id: %d]" % (num, update.text, update.id)
# Ask the user which tweet to start with.
while True:
    start_tweet_num = int(raw_input("Start with which tweet: "))
    if 0 <= start_tweet_num <= len(recent_updates)-1:
        break;
    else:
        print "Invalid selection."
# Get the id of the tweet *before* the starting tweet b/c we'll use this as
# the `since_id` when grabbing tweets from the queue timeline.
last_id = recent_updates[start_tweet_num+1].id

while True:
    # Make sure it's between 8 am and 10 pm.
    cur_hour = time.localtime().tm_hour
    if not (cur_hour >= 8 and cur_hour < 22):
        print "It's too late to tweet!"
        time.sleep(60*10)
        continue
    # Sleep if we're near our rate limit.
    if api.GetRateLimitStatus()["remaining_hits"] < 10:
        print "Rate limiting..."
        time.sleep(600)
        continue
    # Check the buffer stream for new tweets, and post the oldest new tweet.
    print "Checking..."
    untweeted = api.GetUserTimeline(screen_name=bbconfig.queue_username, since_id=last_id)
    if len(untweeted) > 0:
        to_post = untweeted[-1]
        api.PostUpdate(to_post.text)
        last_id = to_post.id
        print "Tweeting: %s [id: %d]" % (to_post.text, last_id)
        # Save last tweet id to file in case the script gets killed.
        with open(".last_tweet_id", 'w') as id_file:
            id_file.write(str(last_id))
    # Sleep between checks/posts.
    time.sleep(bbconfig.check_interval)
